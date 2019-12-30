import logging
import os
from functools import lru_cache

from duckling import DucklingWrapper
from nose.tools import assert_is_not_none

from ohri.hub.logger.duckling_logger import DucklingLogger
from ohri.tool.performance.performance_tool import PerformanceTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
FILE_NAME = os.path.basename(FILE_PATH)

logger = DucklingLogger.filename_level2logger(FILE_NAME, logging.DEBUG)


class DucklingTool:
    class Dim: # following duckling terminology
        TIME = "time"
        TIMEZONE = "timezone"
        TEMPERATURE = "temperature"
        NUMBER = "number"
        ORDINAL = "ordinal"
        DISTANCE = "distance"
        VOLUME = "volume"
        MONEY = "money"
        DURATION = "duration"
        EMAIL = "email"
        URL = "url"
        PHONE_NUMBER = "phone_number"
        LEVEN_PRODUCT = "leven_product"
        LEVEN_UNIT = "leven_unit"
        QUANTITY = "quantity"
        CYCLE = "cycle"
        UNIT = "unit"
        UNIT_OF_DURATION = "unit_of_duration"

    @classmethod
    @lru_cache(maxsize=2)
    @PerformanceTool.profile_duration(logger=logger)
    def duckling(cls):
        return DucklingWrapper()


    @classmethod
    def _dim2func(cls, d, dim):
        h = {cls.Dim.TIME: d.parse_time,
             cls.Dim.TIMEZONE: d.parse_timezone,
             cls.Dim.TEMPERATURE: d.parse_temperature,
             cls.Dim.NUMBER: d.parse_number,
             cls.Dim.ORDINAL: d.parse_ordinal,
             cls.Dim.DISTANCE: d.parse_distance,
             cls.Dim.VOLUME: d.parse_volume,
             cls.Dim.MONEY: d.parse_money,
             cls.Dim.DURATION: d.parse_duration,
             cls.Dim.EMAIL: d.parse_email,
             cls.Dim.URL: d.parse_url,
             cls.Dim.PHONE_NUMBER: d.parse_phone_number,
             cls.Dim.LEVEN_PRODUCT: d.parse_leven_product,
             cls.Dim.LEVEN_UNIT: d.parse_leven_unit,
             cls.Dim.QUANTITY: d.parse_quantity,
             cls.Dim.CYCLE: d.parse_cycle,
             cls.Dim.UNIT: d.parse_unit,
             cls.Dim.UNIT_OF_DURATION: d.parse_unit_of_duration,
             }

        return h.get(dim)


    @classmethod
    @PerformanceTool.profile_duration(logger=logger)
    def str_dim2parse(cls, d, str_in, dim):
        f = cls._dim2func(d,dim)
        assert_is_not_none(f, {"str_in":str_in, "dim":dim})

        return f(str_in)

