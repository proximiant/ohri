import logging
import os
from datetime import datetime
from functools import lru_cache
from itertools import chain

from duckling import DucklingWrapper
from nose.tools import assert_is_not_none

from ohri.hub.logger.duckling_logger import DucklingLogger
from ohri.tool.collection.collection_tool import luniq, lmap
from ohri.tool.json.json_tool import jdown
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

    @classmethod
    def parse2value(cls, p):
        return jdown(p, ["value", "value"])

    @classmethod
    def _parse2other_list(cls, p):
        other_list = jdown(p, ["value", "others"])
        if not other_list:
            return []

        return [o.get("value") for o in other_list]

    @classmethod
    def parse2value_list(cls, p):
        v = cls.parse2value(p)
        other_list = cls._parse2other_list(p)
        l = luniq(chain([v], other_list))
        return l

    # @classmethod
    # def parse_list2value_list(cls, p_list):
    #     return luniq(chain(*lmap(cls.parse2value_list, p_list)))

    @classmethod
    def value2norm_time(cls, v):
        if not v:
            return None

        dt = datetime.fromisoformat(v)
        return dt.time().isoformat()

    @classmethod
    def parse2norm_time_list(cls, parse):
        value_list = DucklingTool.parse2value_list(parse)
        time_list = luniq(filter(bool, map(cls.value2norm_time, value_list)))

        parse_norm = parse.copy()
        parse_norm.update({"value": time_list})
        return parse_norm


