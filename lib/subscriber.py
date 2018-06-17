from .socket import Socket
from .logger import Logger
from .events import Events
from .constants import Constants

class Subscriber(Socket):
    #
    def __init__(self, name=None, host=None, port=None, protocol=None):
        super(Subscriber, self).__init__(host, port, protocol)
        self.name = name if name is not None else Constants.ANONYMOUS
        Logger.debug("creating subscriber: " + self.name)

    def send_identification_info(self):
        self.send_message('CONSUMER', {'name': self.name})