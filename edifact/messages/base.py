# -*- coding: utf-8 -*-
"""This module provides the base for message wrappers."""

import six


class MessageMeta(type):
    """Meta class for segments."""

    def __new__(cls, name, bases, attrs):
        """Create class."""
        return super(MessageMeta, cls).__new__(cls, name, bases, attrs)


class Message(six.with_metaclass(MessageMeta)):
    """Base class for segments."""

    total_number_of_segments = 32

    def __init__(self, una, src_string=None):
        """Constructor."""
