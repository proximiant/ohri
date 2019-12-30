import logging
import os

from ohri.hub.logger.duckling_logger import DucklingLogger
from ohri.tool.duckling_tool import DucklingTool
from ohri.tool.performance.performance_tool import PerformanceTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
FILE_NAME = os.path.basename(FILE_PATH)

DucklingLogger.attach_stderr2loggers(logging.DEBUG)
logger = DucklingLogger.filename_level2logger(FILE_NAME, logging.DEBUG)

@PerformanceTool.profile_duration(logger=logger)
def str2time_entity():
    d = DucklingTool.duckling()
    print(d.parse_time(u'Let\'s meet at 11:45am'))
    # [{u'dim': u'time', u'end': 21, u'start': 11, u'value': {u'value': u'2016-10-14T11:45:00.000-07:00', u'others': [u'2016-10-14T11:45:00.000-07:00', u'2016-10-15T11:45:00.000-07:00', u'2016-10-16T11:45:00.000-07:00']}, u'text': u'at 11:45am'}]


@PerformanceTool.profile_duration(logger=logger)
def str2temperature_entity():
    d = DucklingTool.duckling()
    print(d.parse_time(u'Let\'s meet at 11:45am'))
    # [{u'dim': u'temperature', u'end': 65, u'start': 55, u'value': {u'unit': u'degree', u'value': 65.0}, u'text': u'65 degrees'}, {u'dim': u'temperature', u'end': 51, u'start': 33, u'value': {u'unit': u'celsius', u'value': 32.0}, u'text': u'thirty two celsius'}]

def main():
    d = DucklingTool.duckling()

    str2time_entity()
    str2temperature_entity()

if __name__ == '__main__':
    main()
