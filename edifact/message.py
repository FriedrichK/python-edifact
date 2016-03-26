# -*- coding: utf-8 -*-
"""This module provides the wrappers for basic EDIFACT components."""


def contains_una(input_string):
    """Return True if the message contains the optional UNA segment, False if not."""
    return input_string[:3] == 'UNA'


class Message(object):
    """Wrapper class for EDIFACT messages."""

    una = None

    def __init__(self, src_string=None):
        """Constructor."""
        if src_string:
            self.init_from_string(src_string)

    def init_from_string(self, src_string):
        """Initialize from string source."""
        # Set UNA, optionally from source
        if contains_una(src_string):
            una = UNA(src_string)
        else:
            una = UNA()
        self.una = una


class UNA(object):
    """Wrapper class for UNA (Service String Advice) components."""

    component_data_element_separator = ':'  # pylint: disable=invalid-name
    data_element_separator = '+'
    decimal_mark = ','
    release_character = '?'
    segment_terminator = '\''

    @staticmethod
    def is_valid_una_string(input_string):
        """Return True if input_string is valid, False if not."""
        if not input_string[:3] == 'UNA':
            input_string = 'UNA' + input_string

        if not input_string:
            return False
        if len(input_string) < 9:
            return False
        if not input_string[7] == ' ':
            return False
        return True

    def __init__(self, src_string=None):
        """Constructor."""
        if src_string:
            self.init_from_string(src_string)

    def init_from_string(self, src_string):
        """Initialize from string source."""
        if not src_string:
            raise ValueError('empty source string')
        if len(src_string) < 9:
            raise ValueError('source string too short')
        if not src_string[7] == ' ':
            raise ValueError('source string has to have a space at index 4')

        self.component_data_element_separator = src_string[3]  # pylint: disable=invalid-name
        self.data_element_separator = src_string[4]
        self.decimal_mark = src_string[5]
        self.release_character = src_string[6]
        self.segment_terminator = src_string[8]

    def get_una_string(self):
        """Get string representation of UNA."""
        return 'UNA{0}{1}{2}{3} {4}'.format(
            self.component_data_element_separator,
            self.data_element_separator,
            self.decimal_mark,
            self.release_character,
            self.segment_terminator,
        )


class UNB(object):
    """Wrapper class for UNB (Interchange Header) components."""

    def __init__(self, src_string=None):
        """Constructor."""
        if src_string:
            self.init_from_string(src_string)

    def init_from_string(self, src_string):
        """Initialize from string source."""
        if not src_string:
            raise ValueError('empty source string')
