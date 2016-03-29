"""Tests the core functionality."""

import unittest

from edifact.helpers import separate_segments, separate_components 


class HelperTest(unittest.TestCase):
    """Test helper functions."""

    def test_separates_segments_as_expected_with_release_character_and_newline(self):
        src_string="UNH+1+MSCONS:D:01B:UN:EAN004'\nBGM+94E::9+6078+9' NAD+SU+++Papa John?'s'"
        expected = ["UNH+1+MSCONS:D:01B:UN:EAN004'", "BGM+94E::9+6078+9'", "NAD+SU+++Papa John?'s'"]
        actual = separate_segments(src_string)
        self.assertEqual(actual, expected)

    def test_separates_components_as_expected_with_release_character(self):
        src_string="NAD+SU+++Papa John?'s:business:food:pizza'"
        expected = ["NAD", "SU", "", "", ["Papa John?'s", "business", "food", "pizza"]]
        actual = separate_components(src_string)
        self.assertEqual(actual, expected)
