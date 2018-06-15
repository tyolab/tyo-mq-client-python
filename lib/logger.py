#
#

class Logger:
    instance = None

    def __init__(self, level):
        self.level = level

    @staticmethod
    def log(msg):
        print (msg)

    @staticmethod
    def error(msg):
        print (msg)

    @staticmethod
    def warn(msg):
        print (msg)

    @staticmethod
    def verbose(msg):
        print (msg)

    @staticmethod
    def debug(msg):
        print (msg)

    @staticmethod
    def info(msg):
        print (msg)