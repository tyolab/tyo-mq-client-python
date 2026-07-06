from .publisher import Publisher
from .subscriber import Subscriber
from .socket import Socket


class MessageQueue(object):
    """Factory for tyo-mq producers and consumers.

        mq = MessageQueue(host='localhost', port=17352)
        # with auth enabled on the server:
        mq = MessageQueue(auth={'token': 'my-token'})
    """

    def __init__(self, host=None, port=None, protocol=None, logger=None, auth=None):
        self.host = host
        self.port = port
        self.protocol = protocol
        self.logger = logger
        self.auth = auth

    def __merged(self, host, port, protocol, logger, auth):
        return (
            host if host is not None else self.host,
            port if port is not None else self.port,
            protocol if protocol is not None else self.protocol,
            logger if logger is not None else self.logger,
            auth if auth is not None else self.auth,
        )

    def createSocket(self, host=None, port=None, protocol=None, logger=None, auth=None):
        h, p, ptc, lg, a = self.__merged(host, port, protocol, logger, auth)
        return Socket(h, p, ptc, lg, a)

    def createConsumer(self, name, host=None, port=None, protocol=None, logger=None, auth=None):
        h, p, ptc, lg, a = self.__merged(host, port, protocol, logger, auth)
        return Subscriber(name, h, p, ptc, lg, a)

    # Alias of createConsumer
    def createSubscriber(self, name, host=None, port=None, protocol=None, logger=None, auth=None):
        return self.createConsumer(name, host, port, protocol, logger, auth)

    def createProducer(self, name, eventDefault=None, host=None, port=None, protocol=None, logger=None, auth=None):
        h, p, ptc, lg, a = self.__merged(host, port, protocol, logger, auth)
        return Publisher(name, eventDefault, h, p, ptc, lg, a)

    def createPublisher(self, name, eventDefault=None, host=None, port=None, protocol=None, logger=None, auth=None):
        return self.createProducer(name, eventDefault, host, port, protocol, logger, auth)
