#!/usr/bin/env python
"""
test.py: run available tests
"""

import coverage
import unittest
import os
import sys


if '__main__' == __name__:
    pattern = 'test_*.py'

    if 2 > len(sys.argv):
        _coverage = coverage.coverage()
        _coverage.start()
    elif 2 < len(sys.argv):
        pattern = 'test_{}_{}.py'.format(sys.argv[1], sys.argv[2])
    else:
        pattern = 'test_{}_*.py'.format(sys.argv[1])

    sys.path.append(os.path.dirname('..'))

    unittest.TextTestRunner(verbosity=1).run(
        unittest.TestLoader().discover('src.tests', pattern=pattern)
    )

    if 2 > len(sys.argv):
        _coverage.stop()
        _coverage.save()
        _coverage.report()
        _coverage.html_report()
