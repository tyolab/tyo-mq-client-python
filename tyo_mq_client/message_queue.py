#
#
from .constants import Constants
from .publisher import Publisher
from .subscriber import Subscriber
from .socket import Socket
from .events import Events
from .logger import Logger

class MessageQueue(object):

    def __init__(self, host=None, port=None, protocol=None, logger=None):
        # The SocketIO instance
        self.host = host
        self.port = port
        self.protocol = protocol        
        self.logger = logger    

    def createSocket(self, host=None, port=None, protocol=None, logger=None):
        mySocket = Socket(host if host is not None else self.host, port if port is not None else self.port, protocol if protocol is not None else self.protocol, logger)
        return mySocket

    #/**
     #* private function
     #*/
    def __createConsumerPrivate(self, name, host=None, port=None, protocol=None, logger=None): 
        consumer = Subscriber(name, host if host is not None else self.host, port if port is not None else self.port, protocol if protocol is not None else self.protocol, logger)
        return consumer


    # /**
    #  * Create a consumer
    #  */
    def createConsumer(self, name, host=None, port=None, protocol=None, logger=None):
        return self.__createConsumerPrivate(name, host, port, protocol, logger)

    # /**
    #  * Alias of createConsumer
    #  */

    def createSubscriber(self, name, host=None, port=None, protocol=None, logger=None):
        return self.createConsumer(name, host, port, protocol, logger)

    def __createProducerPrivate (self, name, eventDefault=None, host=None, port=None, protocol=None, logger=None):
        h = host if host is not None else self.host
        p = port if port is not None else self.port
        ptc = protocol if protocol is not None else self.protocol

        producer = Publisher(name, eventDefault, h, p, ptc, logger)
        return producer
     
    # /**
    #  * Create a producer
    #  */
    def createProducer (self, name, eventDefault=None, host=None, port=None, protocol=None, logger=None):
        return  self.__createProducerPrivate(name, eventDefault, host, port, protocol, logger)

    def createPublisher (self, name, eventDefault=None, host=None, port=None, protocol=None, logger=None):
        return self.createProducer(name, eventDefault, host, port, protocol, logger)