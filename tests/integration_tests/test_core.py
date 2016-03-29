"""Tests the core functionality."""

import unittest

from helpers import load_edifact_sample

from edifact import from_string


class ParseTest(unittest.TestCase):
    """Test the parse functionality."""

    def test_returns_expected_segment_count(self):
        mscons_sample = load_edifact_sample('edifact_sample_mscons_1.txt')
        mscons = from_string(mscons_sample)
        self.assertEqual(mscons.total_number_of_segments, 32)
