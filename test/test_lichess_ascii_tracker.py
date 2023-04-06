#!/usr/bin/python3
"""
Test
"""

import sys
import os
import unittest
from lichess_ascii_tracker import usage

sys.path.insert(0, os.path.dirname(__file__))


class Testing(unittest.TestCase):
    """
    Testing lichess_ascii_tracker
    """

    def test_usage(self):
        """
        first temp test
        """
        usage()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
