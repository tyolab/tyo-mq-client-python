"""
Python implementation of the tyostocks Logger class.

This module provides a flexible logger that can output colored logs to the
console and write to files, similar to its JavaScript counterpart.
"""
from enum import IntEnum
import logging
import sys
import os
from datetime import datetime


class ColoredFormatter(logging.Formatter):
    """
    A custom log formatter that adds color to log messages based on level.
    """
    BLUE = '\x1b[34m'
    GREEN = '\x1b[32m'
    YELLOW = '\x1b[33m'
    RED = '\x1b[31m'
    BOLD_RED = '\x1b[31;1m'
    RESET = '\x1b[0m'

    LEVEL_COLORS = {
        logging.DEBUG: BLUE,
        logging.INFO: GREEN,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: BOLD_RED,
    }

    def __init__(self, fmt="[%(name)s|%(asctime)s] %(levelname)s: %(message)s", datefmt='%Y-%m-%d %H:%M:%S'):
        super().__init__(datefmt=datefmt)
        self.base_fmt = fmt

    def format(self, record):
        color = self.LEVEL_COLORS.get(record.levelno, self.RESET)
        log_fmt = f"[{record.name}|%(asctime)s] {color}%(levelname)-8s{self.RESET} %(message)s"
        formatter = logging.Formatter(log_fmt, self.datefmt)
        return formatter.format(record)

class LogLevel(IntEnum):
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    WARN = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET

class Logger:
    """
    A Python implementation of the tyostocks Logger class.

    It provides leveled, colored logging to the console and can also write
    logs to one or more files.

    Usage:
        logger = Logger('my_app', level='DEBUG', logger_file='app.log')
        logger.info("This is an info message.")
        logger.error("This is an error message.")
    """

    _STRING_TO_LEVEL = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'WARN': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'NOTSET': logging.NOTSET,
    }

    def __init__(self, name, level=None, logger_file=None, errors_file=None, out=sys.stdout):
        """
        Initializes the Logger.

        Args:
            name (str): The name of the logger.
            level: The logging level. Can be a string or an integer. Defaults to INFO.
            logger_file (str, optional): Path to the general log file. Defaults to None.
            errors_file (str, optional): Path to the error log file. Defaults to None.
            out (stream, optional): The output stream for console logging. Defaults to sys.stdout.
        """
        self.name = name
        self._logger = logging.getLogger(name)

        if self._logger.hasHandlers():
            self._logger.handlers.clear()

        self._logger.propagate = False
        
        self.level = None
        self.set_level(level if level is not None else 'INFO')

        # Console handler
        self.console_handler = logging.StreamHandler(out)
        self.console_handler.setFormatter(ColoredFormatter())
        self._logger.addHandler(self.console_handler)

        # File handlers
        self.logger_file = None
        self.file_handler = None
        self.errors_file = None
        self.error_handler = None

        if logger_file:
            self.file_start(logger_file)
        if errors_file:
            self.errors_file = errors_file
            self.error_handler = logging.FileHandler(errors_file, mode='a', encoding='utf-8')
            self.error_handler.setLevel(logging.ERROR)
            self.error_handler.setFormatter(
                logging.Formatter('[%(name)s|%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
            self._logger.addHandler(self.error_handler)

    def set_level(self, level):
        """Sets the logging level for the logger."""
        if isinstance(level, LogLevel):
            py_level = level.value
            if py_level is None:
                raise ValueError(f"Invalid log level: {level}")
            self.level = py_level

        elif isinstance(level, str):
            py_level = self._STRING_TO_LEVEL.get(level.upper())
            if py_level is None:
                raise ValueError(f"Invalid log level string: {level}")
            self.level = py_level
        elif isinstance(level, int):
            self.level = level
        else:
            raise TypeError(f"Level must be a string or an integer, not {type(level)}")
        self._logger.setLevel(self.level)

    def _combine_args(self, *args):
        return ' '.join(map(str, args))

    def log(self, *args, **kwargs):
        self._logger.info(self._combine_args(*args), **kwargs)

    def info(self, *args, **kwargs):
        self._logger.info(self._combine_args(*args), **kwargs)

    def warning(self, *args, **kwargs):
        self._logger.warning(self._combine_args(*args), **kwargs)

    def warn(self, *args, **kwargs):
        self.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        self._logger.error(self._combine_args(*args), exc_info=True, **kwargs)

    def debug(self, *args, **kwargs):
        self._logger.debug(self._combine_args(*args), **kwargs)

    def critical(self, *args, **kwargs):
        self._logger.critical(self._combine_args(*args), **kwargs)

    def output(self, *args, **kwargs):
        self._logger.info(self._combine_args(*args), **kwargs)

    def file_start(self, file, append_only=False):
        """Starts logging to a specified file."""
        self.file_end()  # Close existing handler if any

        if not append_only and os.path.exists(file):
            try:
                os.remove(file)
            except OSError as e:
                self.error(f"Could not remove old log file {file}: {e}")

        self.logger_file = file
        self.file_handler = logging.FileHandler(self.logger_file, mode='a', encoding='utf-8')
        self.file_handler.setFormatter(
            logging.Formatter('[%(name)s|%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
        self._logger.addHandler(self.file_handler)

    def file_end(self):
        """Stops logging to the main log file."""
        if self.file_handler:
            self._logger.removeHandler(self.file_handler)
            self.file_handler.close()
            self.file_handler = None
            self.logger_file = None

    def file_file(self, logger_file, level_string, date, *what):
        """
        Dynamically logs a message to an arbitrary file, similar to the JS version.
        """
        if not logger_file:
            return

        if date is None:
            date = datetime.now()

        message = ' '.join(map(str, what))
        date_str = date.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Format to milliseconds
        log_line = f"[{self.name}|{date_str}] ({level_string}) {message}\n"

        try:
            with open(logger_file, 'a', encoding='utf-8') as f:
                f.write(log_line)
        except Exception as e:
            self._logger.error(f"Failed to write to log file {logger_file}: {e}")
