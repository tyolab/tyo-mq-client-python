#
#
from .subscriber import Subscriber
from .logger import Logger

class Publisher(Subscriber):
    def __init__(self, name, eventDefault=None, host=None, port=None, protocol=None):
        super(Publisher, self).__init__(name, host, port, protocol)
        self.eventDefault = eventDefault
        Logger.debug("creating producer: " + self.name)
    