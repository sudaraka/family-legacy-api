#!/usr/bin/env python
"""
test.py: run available tests
"""

import coverage
import unittest


if '__main__' == __name__:
    _coverage = coverage.coverage()
    _coverage.start()

    unittest.TextTestRunner(verbosity=1).run(
        unittest.TestLoader().discover('src.tests')
    )

    _coverage.stop()
    _coverage.report()
