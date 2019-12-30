import json
import logging
import os
import sys
from unittest import TestCase

from ohri.hub.logger.duckling_logger import DucklingLogger
from ohri.tool.duckling_tool import DucklingTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
FILE_NAME = os.path.basename(FILE_PATH)

DucklingLogger.attach_stderr2loggers(logging.DEBUG)
logger = DucklingLogger.filename_level2logger(FILE_NAME, logging.DEBUG)


class TestDucklingTool(TestCase):
    """ time """
    def test_01(self):
        d = DucklingTool.duckling()
        hyp = DucklingTool.str_dim2parse(d,
                                         u'Let\'s meet at 11:45am',
                                         DucklingTool.Dim.TIME,
                                         )
        ref = [
            {
                "dim": "time",
                "text": "at 11:45am",
                "start": 11,
                "end": 21,
                "value": {
                    "value": "2019-12-30T11:45:00.000-08:00",
                    "grain": "minute",
                    "others": [
                        {
                            "grain": "minute",
                            "value": "2019-12-30T11:45:00.000-08:00"
                        },
                        {
                            "grain": "minute",
                            "value": "2019-12-31T11:45:00.000-08:00"
                        },
                        {
                            "grain": "minute",
                            "value": "2020-01-01T11:45:00.000-08:00"
                        }
                    ]
                }
            }
        ]

        # print(json.dumps({"hyp": hyp}, indent=2), file=sys.stderr)

        self.assertEqual(hyp, ref)

    """ temperature """
    def test_02(self):
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

        # print(json.dumps({"hyp": hyp}, indent=2), file=sys.stderr)
        self.assertEqual(hyp, ref)
