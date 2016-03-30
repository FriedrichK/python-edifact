"""Tests the basic Message functionality."""

import unittest
import mock

from edifact.messages.base import Message


class MessagesBaseTest(unittest.TestCase):

    def test_fails_basic_validation_for_unh(self):
        mock_source_without_unh = "NOPE+1+MSCONS:D:01B:UN:EAN004'BGM+94E::9+6078+9'DTM+137:20020204:102'NAD+SU+5071615111110::9'NAD+BY+5098765111111::9'"
        mock_una = mock.MagicMock()
        self.assertRaises(ValueError, Message, mock_una, src_string=mock_source_without_unh)

    def test_fails_basic_validation_for_bgm(self):
        mock_source_without_unh = "UNH+1+MSCONS:D:01B:UN:EAN004'NOPE+94E::9+6078+9'DTM+137:20020204:102'NAD+SU+5071615111110::9'NAD+BY+5098765111111::9'"
        mock_una = mock.MagicMock()
        self.assertRaises(ValueError, Message, mock_una, src_string=mock_source_without_unh)

    def test_fails_basic_validation_for_unt(self):
        mock_source_without_unh = "UNH+1+MSCONS:D:01B:UN:EAN004'BGM+94E::9+6078+9'DTM+137:20020204:102'NAD+SU+5071615111110::9'NAD+BY+5098765111111::9'"
        mock_una = mock.MagicMock()
        self.assertRaises(ValueError, Message, mock_una, src_string=mock_source_without_unh)