#!/usr/bin/env python
"""
test.py: run available tests
"""

import coverage
import unittest
import os
import sys


if '__main__' == __name__:
    _coverage = coverage.coverage()
    _coverage.start()

    sys.path.append(os.path.dirname('..'))

    unittest.TextTestRunner(verbosity=1).run(
        unittest.TestLoader().discover('src.tests')
    )

    _coverage.stop()
    _coverage.save()
    _coverage.report()
    _coverage.html_report()
