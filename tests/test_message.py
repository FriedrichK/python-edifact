"""Tests the core Message wrapper."""

import unittest
import mock

import os.path

from edifact import message
from edifact.message import Message, UNA

MESSAGE_STRING_WITH_UNA = 'UNA and the rest is irrelevant'
MESSAGE_STRING_WITHOUT_UNA = "no UNA here"


class MessageModuleTest(unittest.TestCase):
    """Test the message module."""

    def testExistenceCheck(self):
        self.assertEqual(message.contains_una(MESSAGE_STRING_WITH_UNA), True)
        self.assertEqual(message.contains_una(MESSAGE_STRING_WITHOUT_UNA), False)


class UNATest(unittest.TestCase):
    """Test the UNA class."""

    def testValidityCheck(self):
        self.assertEqual(UNA.is_valid_una_string('UNA:+.? \''), True)
        self.assertEqual(UNA.is_valid_una_string(''), False)
        self.assertEqual(UNA.is_valid_una_string('UNA:+'), False)
        self.assertEqual(UNA.is_valid_una_string('UNB:+.? \''), False)
        self.assertEqual(UNA.is_valid_una_string('UNA:+.?X\''), False)        

    def testIfUNAIsGeneratedCorrectly(self):
        f = open(os.path.dirname(__file__) + '/../testdata/edifact_dummy.txt')
        edifact_dummy = f.read()

        una = UNA(edifact_dummy)

        expected = 'UNA:+.? \''
        self.assertEqual(una.get_una_string(), expected)


class MessageClassTest(unittest.TestCase):
    """Test the Message class."""

    @mock.patch('edifact.message.UNA')
    def testIfMessageWithUNASegmentIsInitializedAsExpected(self, UNAMock):
        message = Message(MESSAGE_STRING_WITH_UNA)
        UNAMock.assert_called_with(MESSAGE_STRING_WITH_UNA)

    @mock.patch('edifact.message.UNA')
    def testIfMessageWithoutUNASegmentGetsDefaultUNA(self, UNAMock):
        message = Message(MESSAGE_STRING_WITHOUT_UNA)
        UNAMock.assert_called_with()


