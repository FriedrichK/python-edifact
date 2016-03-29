# -*- coding: utf-8 -*-
"""This module provides wrappers for different segment types."""


from edifact.segments.base import Composite, Segment


class DTM(Segment):
    """Date/Time/Period segment."""

    qualifier = Composite(index=0, max_length=3, required=True)
    value = Composite(index=1, max_length=35, required=True)
    format = Composite(index=2, max_length=3, required=True)

    class Meta:
        identifier = 'DTM'
