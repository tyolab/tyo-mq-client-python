#
# 
from .constants import Constants
from .logger import Logger
from .base import Base

from socketIO_client import SocketIO, BaseNamespace
import uuid

class SocketListener(BaseNamespace):

    def on_connect(self):
        print('[Connected]')

    def on_reconnect(self):
        print('[Reconnected]')

    def on_disconnect(self):
        print('[Disconnected]')


class Socket(Base):
    
    #
    def __init__(self, host=None, port=None, protocol=None):
        self.autoreconnect = True
        if (host is None):
            self.host = 'localhost'
        else:
            self.host = host

        if (port is None):
            self.port = Constants.DEFAULT_PORT
        else:
            self.port = port

        if (protocol is not None):
            self.protocol = protocol

        self.socket = None
        self.connected = False
        self.id = uuid.uuid4()
        self.name = Constants.ANONYMOUS;
        self.alias = None

    def on_connect(self):
        print('connect')

    def on_disconnect(self):
        print('disconnect')

    def on_reconnect(self):
        print('reconnect')
        
    #
    def connect(self, duration=-1):
        # Example
        # with SocketIO(self.host, self.port, SocketListener) as socketIO:
        #     socketIO.emit('aaa')
        #     socketIO.wait(seconds=1)
        self.socket = SocketIO(self.host, self.port, SocketListener)
        self.socket.on('connect', self.on_connect)
        self.socket.on('disconnect', self.on_disconnect)
        self.socket.on('reconnect', self.on_reconnect)

        if duration == -1 :
            self.socket.wait()
        else:
            self.socket.wait(seconds=duration)

    def get_id(self):
        return self.id


