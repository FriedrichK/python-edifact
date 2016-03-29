# -*- coding: utf-8 -*-
"""Provides core functions."""

from edifact.configuration import MESSAGE_CLASSES

from edifact.message_headers.una import UNA
from edifact.message_headers.unh import UNH

from edifact.messages.un import *


def from_string(edifact_string):
    """Create a Message from an EDIFACT string."""
    una = extract_una_or_generate_default(edifact_string)
    unh = UNH(una=una, src_string=edifact_string)

    message_class = MESSAGE_CLASSES[unh.get('message_type')]

    return message_class(una, src_string=edifact_string)


def extract_una_or_generate_default(edifact_string):
    """Extract the UNA segment or generate a default one."""
    if edifact_string[:3] == 'UNA':
        return UNA(src_string=edifact_string[:9])
    else:
        return UNA()
