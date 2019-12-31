import logging
import os
from datetime import time
from functools import reduce
from pprint import pprint
from unittest import TestCase

from future.utils import lmap

from ohri.hub.logger.duckling_logger import DucklingLogger
from ohri.tool.collection.collection_tool import luniq
from ohri.tool.duckling.duckling_tool import DucklingTool
from ohri.tool.testing.testing_tool import TestingTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
FILE_NAME = os.path.basename(FILE_PATH)

DucklingLogger.attach_stderr2loggers(logging.DEBUG)
logger = DucklingLogger.filename_level2logger(FILE_NAME, logging.DEBUG)


def hyp2norm_time_list(hyp):
    return lmap(DucklingTool.parse2norm_time_list, hyp)

class TestDucklingTool(TestCase):

    """ time """
    def test_01(self):
        d = DucklingTool.duckling()
        hyp = DucklingTool.str_dim2parse(d,
                                         u'Let\'s meet at 11:45am',
                                         DucklingTool.Dim.TIME,
                                         )

        ref = [{'dim': 'time',
                'end': 21,
                'start': 11,
                'text': 'at 11:45am',
                'value': ['11:45:00']}]

        # pprint(hyp2norm_time_list(hyp))

        self.assertEqual(hyp2norm_time_list(hyp), ref)

    def test_02(self):
        d = DucklingTool.duckling()
        hyp = DucklingTool.str_dim2parse(d,
                                         u'at two',
                                         DucklingTool.Dim.TIME,
                                         )
        ref = [{'dim': 'time',
                'end': 6,
                'start': 0,
                'text': 'at two',
                'value': ['02:00:00', '14:00:00']}]

        # pprint(hyp2norm_time_list(hyp))

        self.assertEqual(hyp2norm_time_list(hyp), ref)

    @TestingTool.expected_failure_deco(reason="Alexa script variation support not expected")
    def test_03(self):
        d = DucklingTool.duckling()
        hyp = DucklingTool.str_dim2parse(d,
                                         u'1010',
                                         DucklingTool.Dim.TIME,
                                         )
        ref = [
            {
                "dim": "time",
                "text": "1010",
                "start": 0,
                "end": 4,
                "value": ['10:10:00', '22:10:00']}]

        # pprint(hyp2norm_time_list(hyp))

        self.assertEqual(hyp2norm_time_list(hyp), ref)

    def test_04(self):
        d = DucklingTool.duckling()
        hyp = DucklingTool.str_dim2parse(d,
                                         u'10 pm',
                                         DucklingTool.Dim.TIME,
                                         )
        ref = [{'dim': 'time', 'text': '10 pm', 'start': 0, 'end': 5, 'value': ['22:00:00']}]

        # pprint(hyp2norm_time_list(hyp))

        self.assertEqual(hyp2norm_time_list(hyp), ref)

    @TestingTool.expected_failure_deco(reason="'two thirty' type not supported")
    def test_05(self):
        d = DucklingTool.duckling()
        hyp = DucklingTool.str_dim2parse(d,
                                         u'two thirty',
                                         DucklingTool.Dim.TIME,
                                         )
        ref = [{'dim': 'time', 'text': 'two thirty', 'start': 0, 'end': 10, 'value': ['2:30:00', '14:30:00']}]

        # pprint(hyp2norm_time_list(hyp))

        self.assertEqual(hyp2norm_time_list(hyp), ref)

    def test_06(self):
        d = DucklingTool.duckling()
        hyp = DucklingTool.str_dim2parse(d,
                                         u'ten to two',
                                         DucklingTool.Dim.TIME,
                                         )
        ref = [{'dim': 'time',
                'end': 10,
                'start': 0,
                'text': 'ten to two',
                'value': ['01:50:00', '13:50:00']}]

        # pprint(hyp2norm_time_list(hyp))

        self.assertEqual(hyp2norm_time_list(hyp), ref)


    def test_07(self):
        d = DucklingTool.duckling()
        hyp = DucklingTool.str_dim2parse(d,
                                         u'five past ten',
                                         DucklingTool.Dim.TIME,
                                         )
        ref = [{'dim': 'time',
                'end': 13,
                'start': 0,
                'text': 'five past ten',
                'value': ['22:05:00', '10:05:00']}]

        # pprint(hyp2norm_time_list(hyp))

        self.assertEqual(hyp2norm_time_list(hyp), ref)

    """ timezone """
    def test_11(self):
        d = DucklingTool.duckling()
        hyp = DucklingTool.str_dim2parse(d,
                                         u'pst',
                                         DucklingTool.Dim.TIMEZONE,
                                         )
        ref = [{'dim': 'timezone',
                'end': 3,
                'start': 0,
                'text': 'pst',
                'value': {'value': 'PST'}}]

        # pprint(hyp)

        self.assertEqual(hyp, ref)

    @TestingTool.expected_failure_deco(reason="'Asia/Seoul' type timezone not supported")
    def test_12(self):
        d = DucklingTool.duckling()
        hyp = DucklingTool.str_dim2parse(d,
                                         u'Asia/Seoul',
                                         DucklingTool.Dim.TIMEZONE,
                                         )
        ref = [{'dim': 'timezone',
                'end': 3,
                'start': 0,
                'text': 'pst',
                'value': {'value': 'Asia/Seoul'}}]

        # pprint(hyp)

        self.assertEqual(hyp, ref)


    def test_13(self):
        d = DucklingTool.duckling()
        hyp = DucklingTool.str_dim2parse(d,
                                         u'pt',
                                         DucklingTool.Dim.TIMEZONE,
                                         )
        ref = [{'dim': 'timezone',
                'end': 2,
                'start': 0,
                'text': 'pt',
                'value': {'value': 'PT'}}]

        # pprint(hyp)

        self.assertEqual(hyp, ref)

    @TestingTool.expected_failure_deco(reason="'pacific time' type timezone not supported")
    def test_14(self):
        d = DucklingTool.duckling()
        hyp = DucklingTool.str_dim2parse(d,
                                         u'pacific time',
                                         DucklingTool.Dim.TIMEZONE,
                                         )
        ref = [{'dim': 'timezone',
                'end': 12,
                'start': 0,
                'text': 'pacific time',
                'value': {'value': 'PT'}}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)




    """ temperature """
    def test_21(self):
        d = DucklingTool.duckling()
        hyp = DucklingTool.str_dim2parse(d,
                                         u'Let\'s change the temperatur from thirty two celsius to 65 degrees',
                                         DucklingTool.Dim.TEMPERATURE,)
        ref = [{u'dim': u'temperature',
                u'end': 65,
                u'start': 55,
                u'value': {u'unit': u'degree', u'value': 65.0},
                u'text': u'65 degrees',
                },
               {u'dim': u'temperature',
                u'end': 51,
                u'start': 33,
                u'value': {u'unit': u'celsius', u'value': 32.0},
                u'text': u'thirty two celsius'}
               ]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_22(self):
        d = DucklingTool.duckling()
        hyp = DucklingTool.str_dim2parse(d,
                                         u'forty two degrees',
                                         DucklingTool.Dim.TEMPERATURE,)
        ref = [{'dim': 'temperature',
                'end': 17,
                'start': 0,
                'text': 'forty two degrees',
                'value': {'unit': 'degree', 'value': 42.0}}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)


    """ number """
    def test_31(self):
        d = DucklingTool.duckling()
        hyp = DucklingTool.str_dim2parse(d,
                                         "thirty two",
                                         DucklingTool.Dim.NUMBER, )
        ref = [{'dim': 'number',
                'end': 10,
                'start': 0,
                'text': 'thirty two',
                'value': {'value': 32.0}}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    def test_32(self):
        d = DucklingTool.duckling()
        hyp = DucklingTool.str_dim2parse(d,
                                         "4,320", # comma supported !
                                         DucklingTool.Dim.NUMBER, )
        ref = [{'dim': 'number',
                'end': 5,
                'start': 0,
                'text': '4,320',
                'value': {'value': 4320.0}}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    @TestingTool.expected_failure_deco(reason="'two and a half' not supported. required for age for clothes")
    def test_33(self):
        d = DucklingTool.duckling()
        hyp = DucklingTool.str_dim2parse(d,
                                         "two and a half",
                                         DucklingTool.Dim.NUMBER, )
        ref = [{'dim': 'number',
                'end': 14,
                'start': 0,
                'text': 'two and a half',
                'value': {'value': 2.5}}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    @TestingTool.expected_failure_deco(reason="'three quarters' not supported. required for time.")
    def test_34(self):
        d = DucklingTool.duckling()
        hyp = DucklingTool.str_dim2parse(d,
                                         "three quarters",
                                         DucklingTool.Dim.NUMBER, )
        ref = [{'dim': 'number',
                'end': 14,
                'start': 0,
                'text': 'two and a half',
                'value': {'value': 2.5}}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    @TestingTool.expected_failure_deco(reason="'second one'. 'one' as number")
    def test_35(self):
        d = DucklingTool.duckling()
        hyp = DucklingTool.str_dim2parse(d,
                                         "second one",
                                         DucklingTool.Dim.NUMBER, )
        ref = []

        # pprint(hyp)
        self.assertEqual(hyp, ref)



    """ ordinal """
    def test_41(self):
        d = DucklingTool.duckling()
        hyp = DucklingTool.str_dim2parse(d,
                                         "third",
                                         DucklingTool.Dim.ORDINAL, )
        ref = [{'dim': 'ordinal',
                'end': 5,
                'start': 0,
                'text': 'third',
                'value': {'value': 3}}]

        # pprint(hyp)
        self.assertEqual(hyp, ref)

    @TestingTool.expected_failure_deco(reason="'one second'. 'second' is not ordinal")
    def test_42(self):
        d = DucklingTool.duckling()
        hyp = DucklingTool.str_dim2parse(d,
                                         "one second",
                                         DucklingTool.Dim.ORDINAL, )
        ref = []

        # pprint(hyp)
        self.assertEqual(hyp, ref)



    """ distance """
    """ volume """
    """ money """
    """ duration """
    """ email """
    """ url """
    """ phone_number """
    """ level_product """
    """ leven_unit """
    """ quantity """
    """ cycle """
    """ unit """
    """ unit_of_duration """

