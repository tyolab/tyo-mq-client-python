from .subscriber import Subscriber
from .constants import Constants
from .events import Events

import json
import math
import uuid as _uuid


class Publisher(Subscriber):
    def __init__(self, name, eventDefault=None, host=None, port=None, protocol=None, logger=None, auth=None):
        super(Publisher, self).__init__(name, host, port, protocol, logger, auth)

        self.type = 'PRODUCER'
        self.eventDefault = eventDefault if eventDefault is not None \
            else Events.to_event_string(Constants.EVENT_DEFAULT, self.name)
        self.on_subscription_listener = None
        self.subscribers = {}

        self.add_on_connect_listener(lambda: self.set_on_subscription_listener())

        self.logger.debug("creating producer: " + self.name)

    def send_identification_info(self):
        self.send_message(self.type, {'name': self.name, 'id': self.get_id()})

    def broadcast(self, data, event=None, group=None):
        """Deliver one copy to every member of the realm — or, when `group`
        is given, to every member of that consumer group."""
        options = {'broadcast': 'group' if group else 'realm'}
        if group:
            options['group'] = group
        self.produce(data, event, options=options)

    def produce(self, data, event=None, method=None, options=None):
        """Publish `data` as `event` (or the producer's default event).

        options (all optional):
            broadcast ('realm' | 'group'), group,
            guaranteed (True — persist until consumed), ttl ('1h' or ms)
        """
        if data is None:
            raise Exception("data can't be null")

        if event is None:
            if self.eventDefault is None:
                raise Exception("please specify event")
            event = self.eventDefault

        options = options or {}
        message = {
            "event": event,
            "message": data,
            "from": self.name,
            "method": method if method is not None else Constants.METHOD_UNICAST,
        }
        if options.get('broadcast'):
            message['method'] = Constants.METHOD_BROADCAST
            message['broadcast'] = 'group' if options['broadcast'] == 'group' else 'realm'
            if options.get('group'):
                message['group'] = options['group']
        if options.get('guaranteed'):
            message['guaranteed'] = True
        if options.get('ttl') is not None:
            message['ttl'] = options['ttl']

        full_json = json.dumps(message)

        if len(full_json) <= Constants.CHUNK_SIZE:
            self.send_message('PRODUCE', message)
            return

        # Large message — split into chunks so each frame stays under the limit
        chunk_size = Constants.CHUNK_SIZE
        total = math.ceil(len(full_json) / chunk_size)
        transfer_id = str(_uuid.uuid4()).replace('-', '')

        self.logger.debug("sending large message in " + str(total)
                          + " chunks (transferId: " + transfer_id + ")")

        for i in range(total):
            start = i * chunk_size
            self.send_message('PRODUCE_CHUNK', {
                'transferId': transfer_id,
                'index':      i,
                'total':      total,
                'data':       full_json[start:start + chunk_size]
            })

    #
    # On Subscribe
    #
    def __on_subscription(self, data):
        self.logger.debug("Received subscription information: " + json.dumps(data))

        self.subscribers[data["id"]] = data

        if self.on_subscription_listener is not None:
            self.on_subscription_listener(data)

    def set_on_subscription_listener(self):
        event = Events.to_onsubscribe_event(self.get_id())
        self.on(event, self.__on_subscription)

    #
    # On lost connections with subscriber(s)
    #
    def __on_lost_subscriber(self, callback, data):
        self.logger.warn("Lost subscriber's connection")
        if callback is not None:
            callback(data)

    def set_on_subscriber_lost_listener(self, callback):
        event = Events.to_ondisconnect_event(self.get_id())
        self.on(event, lambda data: self.__on_lost_subscriber(callback, data))

    def on_subscriber_lost(self, callback):
        self.set_on_subscriber_lost_listener(callback)

    #
    # On unsubscribe
    #
    def __on_unsubscribed(self, callback, data):
        if callback is not None:
            callback(data)

    def set_on_unsubscribed_listener(self, event, callback):
        event = Events.to_onunsubscribe_event(event, self.get_id())
        self.on(event, lambda data: self.__on_unsubscribed(callback, data))

    def on_unsubscribed(self, event, callback):
        self.set_on_unsubscribed_listener(event, callback)
