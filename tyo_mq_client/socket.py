from .constants import Constants
from .base import Base

import socketio

import json
import uuid


class Socket(Base):

    def __init__(self, host=None, port=None, protocol=None, logger=None, auth=None):
        super().__init__(logger)
        self.type = 'RAW'

        self.autoreconnect = True
        self.host = host if host is not None else 'localhost'
        self.port = port if port is not None else Constants.DEFAULT_PORT
        self.protocol = protocol if protocol is not None else Constants.DEFAULT_PROTOCOL

        # auth: {'token': ..., 'realm': ..., 'role': ..., 'key': ...}
        # Sent as AUTHENTICATION on connect, before identification — required
        # when the server runs with auth enabled.
        self.auth = auth

        self.socket = None
        self.connected = False
        self.authenticated = False
        self.auth_info = None
        self.id = str(uuid.uuid4())
        self.name = Constants.ANONYMOUS
        self.alias = None

        self.on_connect_listeners = []
        self.on_error_listener = None
        self.on_event_func_list = None


class SocketInitiator():

    def __init__(self, socket_base: Socket):
        self.socket_instance = socket_base
        self.socket_instance.socket = socketio.Client(
            reconnection=True,
            reconnection_attempts=0,   # infinite
            reconnection_delay=1,
            reconnection_delay_max=30,
        )
        self.socket_instance.on('connect', self.on_connect)
        self.socket_instance.on('disconnect', self.on_disconnect)
        self.socket_instance.socket.on(
            'CONSUME_CHUNK',
            lambda chunk: self.socket_instance._handle_consume_chunk(chunk))

    def connect(self, protocol, host, port):
        connection_str = protocol + '://' + host + ':' + str(port) + "/"
        # WebSocket only — matches the Node.js client and avoids polling issues
        # with the server's aggressive pingInterval/pingTimeout.
        self.socket_instance.socket.connect(
            connection_str, transports=['websocket'], wait_timeout=5)

    def on_connect(self):
        self.socket_instance.on_connect()

    def on_disconnect(self):
        self.socket_instance.on_disconnect()


class SocketInstance(Socket):

    def __init__(self, host=None, port=None, protocol=None, logger=None, auth=None):
        super().__init__(host, port, protocol, logger, auth)

        # Pending inbound CONSUME_CHUNK transfers:
        # {transferId: {parts, received, total, event}}
        self.inbound_chunks = {}
        # Direct-dispatch map for assembled chunks: {consumeEventStr: callback}
        self.local_handlers = {}

        self.initiator = SocketInitiator(self)

    def send_identification_info(self):
        self.send_message(self.type, {'name': self.name, 'id': self.get_id()})

    def __has_auth(self):
        a = self.auth
        return a is not None and (a.get('token') or a.get('key')
                                  or a.get('realm') or a.get('role'))

    def __authenticate(self):
        """Send AUTHENTICATION and finish the connect sequence on AUTH_OK.

        Mirrors the Node.js client: identification and queued listeners run
        only after the server accepts the credentials.
        """
        def on_auth_ok(info=None):
            self.authenticated = True
            self.auth_info = info
            self.logger.log("(" + self.name + ") authenticated"
                            + ((" in realm " + info.get('realm')) if isinstance(info, dict) and info.get('realm') else ""))
            self.__after_connect()

        def on_auth_fail(err=None):
            self.logger.error("Authentication failed: " + json.dumps(err))
            if self.on_error_listener is not None:
                self.on_error_listener(err)

        self.socket.on('AUTH_OK', on_auth_ok)
        self.socket.on('AUTH_FAIL', on_auth_fail)

        payload = {}
        for field in ('token', 'realm', 'role', 'key'):
            if self.auth.get(field):
                payload[field] = self.auth[field]
        self.send_message('AUTHENTICATION', payload)

    def __after_connect(self):
        self.send_identification_info()
        for listener in list(self.on_connect_listeners):
            listener()

    def on_connect(self):
        self.logger.log("(" + self.name + ") connected to message queue server")

        self.connected = True
        self.socket.on('ERROR', self.__on_error__)

        if self.__has_auth():
            self.__authenticate()
        else:
            self.__after_connect()

    def on_disconnect(self):
        self.connected = False
        self.authenticated = False
        self.inbound_chunks.clear()
        self.logger.log("Socket (" + self.get_id() + ") is disconnected")

    def on_reconnect(self):
        self.logger.debug('reconnect')

    #
    # On TYO-MQ ERROR MESSAGE
    #
    def __on_error__(self, msg):
        if self.on_error_listener is not None:
            self.on_error_listener(msg)
        else:
            self.logger.error(msg)

    def connect(self, duration=-1, callback=None, **kw):
        self.initiator.connect(self.protocol, self.host, self.port)

    def wait(self):
        """Block the calling thread until the connection is closed."""
        if self.socket is not None:
            self.socket.wait()

    def get_id(self):
        return self.id

    def add_on_connect_listener(self, listener):
        self.on_connect_listeners.append(listener)

    def disconnect(self):
        if self.socket is not None and self.connected:
            self.socket.disconnect()

    def off(self, event):
        self.local_handlers.pop(event, None)
        if self.socket is None:
            raise Exception("Socket is not created yet")
        else:
            self.socket.off(event)

    def on(self, event, callback):
        # Store for direct dispatch by CONSUME_CHUNK reassembly
        self.local_handlers[event] = callback

        if self.socket is None:
            raise Exception("Socket is not created yet")
        else:
            self.socket.on(event, callback)

    def _handle_consume_chunk(self, chunk):
        try:
            transfer_id = chunk['transferId']
            chunk_event = chunk['event']
            index = chunk['index']
            total = chunk['total']
            data = chunk['data']

            if transfer_id not in self.inbound_chunks:
                self.inbound_chunks[transfer_id] = {
                    'parts':    [None] * total,
                    'received': 0,
                    'total':    total,
                    'event':    chunk_event,
                }

            transfer = self.inbound_chunks[transfer_id]
            transfer['parts'][index] = data
            transfer['received'] += 1

            if transfer['received'] == transfer['total']:
                del self.inbound_chunks[transfer_id]
                full_json = ''.join(transfer['parts'])
                try:
                    assembled = json.loads(full_json)
                except Exception as e:
                    self.logger.error("CONSUME_CHUNK: reassembly parse failed: " + str(e))
                    return
                handler = self.local_handlers.get(chunk_event)
                if handler:
                    handler(assembled)
        except Exception as e:
            self.logger.error("CONSUME_CHUNK: processing error: " + str(e))

    def send_message(self, event, msg):
        if self.socket is None:
            raise Exception("Socket isn't initialized yet")

        self.socket.emit(event, msg)
