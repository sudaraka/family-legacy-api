#!/usr/bin/env python
"""
test.py: run available tests
"""

import coverage


_coverage = coverage.coverage()
_coverage.start()

import unittest

unittest.TextTestRunner(verbosity=1).run(
    unittest.TestLoader().discover('src/tests/')
)

_coverage.stop()
_coverage.report()
