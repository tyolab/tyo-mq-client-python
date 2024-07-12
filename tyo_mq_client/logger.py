# filename: logger.py
#

from __future__ import print_function
import sys

from enum import IntEnum

class LogLevel(IntEnum):
    FATAL = 0
    ERROR = 1
    WARN = 2
    VERBOSE = 3
    INFO = 4
    DEBUG = 5
    TRACE = 6

class Logger:
    instance = None

    def __init__(self, name = "logger", level = None):
        Logger.instance = self
        self.name = name
        if level is None:
            self.level = LogLevel.VERBOSE
        else:
            self.level = level

    # @staticmethod
    def log(self, *args, **kwargs):
        if (self.level >= LogLevel.VERBOSE):
            print (args, kwargs)

    # @staticmethod
    def error(self, *args, **kwargs):
        if (self.level >= LogLevel.ERROR):
            print(*args, file=sys.stderr, **kwargs)

    # @staticmethod
    def warn(self, *args, **kwargs):
        if (self.level >= LogLevel.WARN):
            print (args, kwargs)

    # @staticmethod
    def trace(self, *args, **kwargs):
        if (self.level >= LogLevel.TRACE):
            print (args, kwargs)

    # @staticmethod
    def debug(self, *args, **kwargs):
        if (self.level >= LogLevel.DEBUG):
            print (args, kwargs)

    # @staticmethod
    def info(self, *args, **kwargs):
        if (self.level >= LogLevel.INFO):
            print (args, kwargs)