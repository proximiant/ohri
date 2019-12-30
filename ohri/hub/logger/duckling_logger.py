import logging
import os
import sys

from functools import reduce, lru_cache
from itertools import chain

from ohri.tool.function.function_tool import FunctionToolkit

FILE_PATH = os.path.realpath(__file__)
REPO_DIR = reduce(lambda x,f:f(x), [os.path.dirname]*3, FILE_PATH)
LOG_DIR = os.path.join(REPO_DIR,"log")

class DucklingLogFormatter:
    @classmethod
    def format(cls):
        return "%(asctime)s.%(msecs)03d:%(levelname)s:%(filename)s#%(lineno)s:%(name)s:%(message)s"

    @classmethod
    def datefmt(cls):
        return "%Y-%m-%dT%H:%M:%S"

    @classmethod
    def config(cls):
        h = {"format": cls.format(),
             "datefmt": cls.datefmt(), }
        return h

    @classmethod
    def formatter(cls):
        return logging.Formatter(cls.format(), cls.datefmt())


class LoggerTool:
    @classmethod
    def add_or_skip_handlers(cls, logger, handlers):
        if not handlers: return

        for handler in (handlers or []):
            if handler in logger.handlers: continue

            logger.addHandler(handler)

    @classmethod
    def handler_formatter2formatted(cls, handler, formatter):
        handler.setFormatter(formatter)
        return handler

    @classmethod
    def rootname_func2name(cls, rootname, func):
        return ".".join(list(chain([rootname], FunctionToolkit.func2class_func_name_list(func))))

    @classmethod
    def rootname_filename2logger(cls, rootname, filename):
        name = ".".join([rootname,filename])
        logger = logging.getLogger(name)
        return logger


class DucklingLogger:
    ROOTNAME = "davout"

    @classmethod
    def dirpath(cls): return LOG_DIR

    @classmethod
    def _rootname_list(cls):
        return [cls.ROOTNAME]
        #return FoxylibLogger.rootname_list() + [cls.ROOTNAME]

    @classmethod
    def attach_handler2loggers(cls, handler):
        for rootname in cls._rootname_list():
            logger = logging.getLogger(rootname)
            LoggerTool.add_or_skip_handlers(logger, [handler])

    @classmethod
    @lru_cache(maxsize=2)
    def attach_stderr2loggers(cls, level):
        handler = LoggerTool.handler_formatter2formatted(logging.StreamHandler(sys.stderr),
                                                         DucklingLogFormatter.formatter(),
                                                         )
        handler.setLevel(level)
        cls.attach_handler2loggers(handler)


    @classmethod
    def func_level2logger(cls, func, level):
        name = LoggerTool.rootname_func2name(cls.ROOTNAME, func)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        return logger

    @classmethod
    def filename_level2logger(cls, filename, level):
        logger = LoggerTool.rootname_filename2logger(cls.ROOTNAME, filename)
        logger.setLevel(level)
        return logger
