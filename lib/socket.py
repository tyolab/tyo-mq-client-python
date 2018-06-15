#
# 
from .constants import Constants
from .base import Base

from socketIO_client import SocketIO, BaseNamespace

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
    #
    def connect(self):
        with SocketIO(self.host, self.port, SocketListener) as socketIO:
            socketIO.emit('aaa')
            socketIO.wait(seconds=1)
