#
#
from .logger import Logger

class Base(object):
    def __init__(self, logger=None):
        if logger is None:
            self.logger = Logger()
        else:
            self.logger = logger

    def log(self, *args, **kwargs):
        self.logger.log(*args, **kwargs)

    def error(self, *args, **kwargs):
        self.logger.error(*args, **kwargs)

    def warn(self, *args, **kwargs):
        self.logger.warn(*args, **kwargs)

    def trace(self, *args, **kwargs):
        self.logger.trace(*args, **kwargs)

    def debug(self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        self.logger.info(*args, **kwargs)