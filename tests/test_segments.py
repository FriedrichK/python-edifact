"""Tests the segment wrappers."""

import unittest
import mock

from edifact.segments.un import DTM


class DTMSegmentTest(unittest.TestCase):
    """Test the DTM segment."""

    def test_creation(self):
        """Test if the expected string representation is returned"""
        una = mock.MagicMock()
        una.data_element_separator = u'+'
        una.component_data_element_separator = u':'
        una.segment_terminator = u'\''

        dtm = DTM(una, qualifier='137', value='20080706', format='102')

        expected = u'DTM+137:20080706:102\''
        self.assertEquals(unicode(dtm), expected)
