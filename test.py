import sys
import os

import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'tests')))
raise Exception(sys.path)

if __name__ == '__main__':
    testsuite = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=1).run(testsuite)
