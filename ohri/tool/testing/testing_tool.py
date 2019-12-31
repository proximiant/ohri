import unittest
from functools import wraps, reduce

import pytest


class TestingTool:

    @classmethod
    def expected_failure_deco(cls, func=None, reason=None,):
        def wrapper(f):
            wrapper_list = [unittest.expectedFailure,
                            pytest.mark.xfail(reason=reason),
                            ]

            wrapped = reduce(lambda _f, _w: _w(_f), wrapper_list, f)
            return wrapped

        return wrapper(func) if func else wrapper
