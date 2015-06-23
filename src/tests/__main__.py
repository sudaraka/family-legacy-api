""" Run available tests """

import coverage
import unittest
import sys


pattern = 'test_*.py'

if 2 > len(sys.argv):
    _coverage = coverage.coverage()
    _coverage.start()
elif 2 < len(sys.argv):
    pattern = 'test_{}_{}.py'.format(sys.argv[1], sys.argv[2])
else:
    pattern = 'test_{}_*.py'.format(sys.argv[1])

unittest.TextTestRunner(verbosity=1).run(
    unittest.TestLoader().discover('.', pattern=pattern)
)

if 2 > len(sys.argv):
    _coverage.stop()
    _coverage.save()
    _coverage.report()
    _coverage.html_report()
