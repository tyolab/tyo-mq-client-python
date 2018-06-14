#
#

class MessageQueue(object):

    def __init__(self, io):
        # The SocketIO instance
        self.io = io