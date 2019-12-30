import logging
import time
from datetime import datetime
from functools import wraps


class PerformanceTool:
    @classmethod
    def profile_duration(cls, func=None, h_msg_update=None, logger=None, ):

        if h_msg_update is None:
            h_msg_update = {}

        def wrapper(f):
            _logger = logger
            if _logger is None:
                _logger = logging.getLogger(f.__name__)

            @wraps(f)
            def wrapped(*args, **kwargs):

                time_start = time.time()
                result = f(*args, **kwargs)

                time_end = time.time()
                exec_time = time_end - time_start

                h = {"name": '{} Time Profile'.format(f.__name__),
                     "elapsed_time": round(exec_time * 1000, 3),
                     "start": datetime.fromtimestamp(time_start).isoformat(),
                     "end": datetime.fromtimestamp(time_end).isoformat(),
                     }
                if h_msg_update:
                    h.update(h_msg_update)

                _logger.debug(h)

                return result

            return wrapped

        return wrapper(func) if func else wrapper