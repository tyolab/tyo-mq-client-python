from .socket import SocketInstance
from .events import Events
from .constants import Constants

import inspect
import sys


class Subscriber(SocketInstance):

    def __init__(self, name=None, host=None, port=None, protocol=None, logger=None, auth=None):
        super(Subscriber, self).__init__(host, port, protocol, logger, auth)

        self.type = 'CONSUMER'
        self.name = name if name is not None else Constants.ANONYMOUS
        self.consumer_id = self.name
        self.consumes = None
        self.logger.debug("creating subscriber: " + self.name)

    def send_identification_info(self):
        self.send_message(self.type, {
            'name': self.name,
            'id': self.consumer_id,
            'consumer_id': self.consumer_id,
        })

    def __invoke_callback(self, callback, message, from_whom, ack, raw):
        """Call the consume callback with as many arguments as it accepts:
        (message) | (message, from) | (message, from, ack) | (message, from, ack, raw)."""
        try:
            params = inspect.signature(callback).parameters
            has_var = any(p.kind == inspect.Parameter.VAR_POSITIONAL for p in params.values())
            arity = 4 if has_var else len([
                p for p in params.values()
                if p.kind in (inspect.Parameter.POSITIONAL_ONLY,
                              inspect.Parameter.POSITIONAL_OR_KEYWORD)])
        except (TypeError, ValueError):
            arity = 1
        args = (message, from_whom, ack, raw)[:max(1, min(arity, 4))]
        return callback(*args)

    def __on_consume(self, event, obj, options):
        self.logger.debug('received message', event, obj)
        callback = self.consumes.get(event)
        if callback is None:
            return

        message = obj.get('message') if isinstance(obj, dict) else obj
        from_whom = obj.get('from') if isinstance(obj, dict) else None
        msg_id = (obj.get('msgId') or obj.get('msg_id')) if isinstance(obj, dict) else None

        acked = {'done': False}

        def ack():
            if msg_id is None or acked['done']:
                return
            acked['done'] = True
            self.send_message('ACK', {'msgId': msg_id})

        manual_ack = bool(options.get('manual_ack') or options.get('manualAck'))

        try:
            self.__invoke_callback(callback, message, from_whom, ack, obj)
        except Exception:
            # No auto-ACK on a failed handler: the server will retry on its
            # schedule (and dead-letter when attempts are exhausted).
            self.logger.error("Consume handler raised", sys.exc_info()[1])
            return

        if msg_id is not None and not manual_ack:
            ack()

    def __subscribe_internal(self, who, event=None, on_consume_callback=None, options=None):
        options = options or {}

        if options.get('mode') == 'topic' and who is None:
            who = Constants.ALL_PUBLISHERS

        is_all = event is None
        event_str = Events.to_event_string(event) if event is not None else Constants.EVENT_ALL
        scope_str = Constants.SCOPE_ALL if is_all else Constants.SCOPE_DEFAULT

        ack_enabled = bool(options.get('ack') or options.get('require_ack')
                           or options.get('manual_ack') or options.get('manualAck'))

        payload = {
            'event': event_str,
            'producer': who,
            'consumer': self.name,
            'scope': scope_str,
            'consumer_id': options.get('consumer_id', self.consumer_id),
        }
        if options.get('durable'):
            payload['durable'] = True
        if ack_enabled:
            payload['ack'] = True
        if options.get('manual_ack') or options.get('manualAck'):
            payload['manual_ack'] = True
        if options.get('ack_timeout'):
            payload['ack_timeout'] = options['ack_timeout']
        if options.get('retry'):
            payload['retry'] = options['retry']
        if options.get('mode'):
            payload['mode'] = options['mode']
        if options.get('group'):
            payload['group'] = options['group']

        def send_subscription_message():
            self.send_message('SUBSCRIBE', payload)

        # The subscription is (re)sent on every connect; when already
        # connected, send it now.
        if self.connected:
            send_subscription_message()

        if self.consumes is None:
            self.consumes = {}

        consumer_event_str = Events.to_consumer_event(event_str, who, is_all)
        self.consumes[consumer_event_str] = on_consume_callback

        self.logger.debug("setting on event: " + consumer_event_str)
        consume_event_str = Events.to_consume_event(consumer_event_str)
        self.on(consume_event_str,
                lambda data, _e=consumer_event_str, _o=options: self.__on_consume(_e, data, _o))
        return send_subscription_message

    def resubscribe_when_reconnect(self, who, event, on_consume_callback, resubscribe=True, options=None):
        sender = self.__subscribe_internal(who, event, on_consume_callback, options)
        if resubscribe is True:
            self.add_on_connect_listener(sender)

    # Backwards-compatible alias
    resubscribeWhenReconnect = resubscribe_when_reconnect

    def subscribe(self, who, event, on_consume_callback, reconnect=True, options=None):
        """Subscribe to `event` from producer `who`.

        options (all optional, matching the Node.js client):
            durable, ack, manual_ack, ack_timeout ('30s'),
            retry ({'max_attempts': 3, 'delay': '5s', 'backoff': 'exponential'}),
            mode ('topic'), group, consumer_id

        The callback may accept 1–4 positional arguments:
        (message), (message, from), (message, from, ack), (message, from, ack, raw).
        With ack enabled and manual_ack off, deliveries are acknowledged
        automatically after the callback returns without raising.
        """
        # allow subscribe(who, event, cb, options=...) with the dict in
        # the reconnect position, matching loose JS-style call sites
        if isinstance(reconnect, dict) and options is None:
            options = reconnect
            reconnect = options.get('reconnect', True)
        self.resubscribe_when_reconnect(who, event, on_consume_callback, reconnect, options)

    def subscribe_once(self, who, event, on_consume_callback, options=None):
        """Subscribe without re-subscribing after a reconnect."""
        self.subscribe(who, event, on_consume_callback, False, options)

    subscribeOnce = subscribe_once

    def subscribe_all(self, event, on_consume_callback, options=None):
        """Subscribe to `event` from every producer."""
        self.subscribe(Constants.ALL_PUBLISHERS, event, on_consume_callback, True, options)

    subscribeAll = subscribe_all

    def subscribe_topic(self, pattern, on_consume_callback, options=None):
        """Subscribe to an MQTT-style topic pattern from any producer.

        `+` matches one level, `#` matches any trailing levels:
            consumer.subscribe_topic('orders/+/status', handler)
            consumer.subscribe_topic('factory/#', handler, {'durable': True, 'ack': True})
        """
        options = dict(options or {})
        options['mode'] = 'topic'
        self.subscribe(Constants.ALL_PUBLISHERS, pattern, on_consume_callback, True, options)
