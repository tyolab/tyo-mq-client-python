#
#
from .constants import Constants
from .publisher import Publisher
from .subscriber import Subscriber
from .events import Events
from .logger import Logger

class MessageQueue(object):

    def __init__(self, host=None, port=None):
        # The SocketIO instance
        if not host is None:
            self.host = host

        if port is not None:
            self.port = port
