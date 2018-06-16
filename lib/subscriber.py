from .socket import Socket
from .logger import Logger

class Subscriber(Socket):
    #
    def __init__(self, name, host=None, port=None, protocol=None):
        super(Subscriber, self).__init__(host, port, protocol)
        self.name = name
        Logger.debug("creating subscriber: " + self.name)