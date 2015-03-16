#!/usr/bin/env python
"""
test.py: run available tests
"""

import unittest

unittest.TextTestRunner(verbosity=1).run(
    unittest.TestLoader().discover('src/tests/')
)
