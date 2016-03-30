# -*- coding: utf-8 -*-
"""This module provides the base for message wrappers."""

import os

import xml.etree.ElementTree as ET
import six

from edifact.helpers import separate_segments, separate_components, validate_anchor_segments
from edifact.exceptions import MissingSegmentAtPositionError


class MessageMeta(type):
    """Meta class for segments."""

    def __new__(cls, name, bases, attrs):
        """Create class."""
        if 'Meta' in attrs:
            attrs = generate_structure(attrs)
        return super(MessageMeta, cls).__new__(cls, name, bases, attrs)


def generate_structure(attrs):
    xml_spec = get_xml_spec(attrs['Meta'])

    attrs['elements'] = []

    for child in xml_spec.getroot():
        attrs['elements'].append(process_element(child))

    return attrs


def process_element(element):
    if element.tag == 'GROUP':
        return process_group(element)
    else:
        return PlaceholderSegment(element.tag, **element.attrib)


def process_group(element):
    elements = []
    for child in element:
        elements.append(process_element(child))
    return SegmentGroup(elements, **element.attrib)


def get_xml_spec(meta):
    spec_dir = meta.spec_dir if hasattr(meta, 'spec_dir') else os.path.dirname(__file__) + '/specs'
    return ET.parse('{spec_dir}/{spec}.xml'.format(spec_dir=spec_dir, spec=meta.spec))


class Message(six.with_metaclass(MessageMeta)):
    """Base class for segments."""

    total_number_of_segments = 32

    def __init__(self, una, src_string=None):
        """Constructor."""
        if src_string:
            self.initialize_from_src_string(src_string)

    def initialize_from_src_string(self, src_string):
        segments = [separate_components(segment) for segment in separate_segments(src_string)]
        validate_anchor_segments(segments)
        self.process_segments(segments, 0, [0], 0)

    def process_segments(self, segments, segment_index, elements_indices, repeats):
        # Exit at the end of segments or elements
        if segment_index >= len(segments) or len(elements_indices) < 1:
            return

        # Skip certain segments
        segments_to_ignore = ['UNA', 'UNH', 'BGM', 'UNT']
        tag = segments[segment_index][0]
        if tag in segments_to_ignore:
            self.process_segments(segments, segment_index + 1, elements_indices, repeats)

        # Process segment
        segment_or_group = self.get_element(elements_indices)

        # End of group or hierarchy
        if segment_or_group is None:
            segment_index, elements_indices, repeats = self.process_end(segments, segment_index, elements_indices, repeats)

        # Process group
        if isinstance(segment_or_group, SegmentGroup):
            segment_index, elements_indices, repeats = self.process_group(segments, segment_index, elements_indices, repeats)

        # Process segment
        if isinstance(segment_or_group, PlaceholderSegment):
            segment_index, elements_indices, repeats = self.process_segment(segments, segment_index, elements_indices, repeats)

        # Proceed
        self.process_segments(segments, segment_index, elements_indices, repeats)

    def process_end(self, segments, segment_index, elements_indices, repeats):
        # Move one level up
        elements_indices = elements_indices[:-1]

        # Reset a possible repeat cycle
        repeats = 0

        # Return
        return segment_index, elements_indices, repeats

    def process_group(self, segments, segment_index, elements_indices, repeats):
        tag = segments[segment_index][0]
        group = self.get_element(elements_indices)

        # If repeats are exhausted for this group, we stop right there
        if repeats + 1 >= group.repeats:
            elements_indices = elements_indices[:-1]
            repeats = 0
            return segment_index, elements_indices, repeats
        else:
            repeats += 1

        # Group does not have current segment as first segment
        if not group_starts_with_segment(group, tag):

            # Crash is group is mandatory and this is not a repeat attempt
            if group.mandatory and repeats == 0:
                raise MissingSegmentAtPositionError(group.get(0).tag)

            # Otherwise move on
            else:
                elements_indices[-1] += 1

        # Enter group
        else:
            elements_indices.append(0)

        # Return
        return segment_index, elements_indices, repeats

    def process_segment(self, segments, segment_index, elements_indices, repeats):
        tag = segments[segment_index][0]
        segment = self.get_element(elements_indices)

        # Tags don't match
        if not segment.tag == tag:

            # Crash if segment is mandatory and this is not a repeat attempt
            if segment.mandatory and repeats == 0:
                raise MissingSegmentAtPositionError(segment.tag)

            # Otherwise move on
            else:
                elements_indices[-1] += 1

        # Process matching tags
        else:
            # TBD: actual processing
            #print 'match', elements_indices, segment_index, tag

            # Move to next segment
            segment_index += 1

            # Move on to next element if repeats are exhausted or repeat
            if repeats + 1 >= segment.repeats:
                elements_indices[-1] += 1
                repeats = 0
            else:
                repeats += 1

        # Return
        return segment_index, elements_indices, repeats

    def get_element(self, elements_indices):
        if elements_indices[0] >= len(self.elements):
            return None

        result = self.elements[elements_indices[0]]
        for idx in elements_indices[1:]:
            try:
                result = result.get(idx)
            except IndexError:
                result = None
        return result


def group_starts_with_segment(group, tag):
    return group.get(0).tag == tag


# Just for now
class PlaceholderSegment(object):
    def __init__(self, tag, status='M', repeats='1', label=None, description=None):
        self.tag = tag
        self.status = status
        self.mandatory = status == 'M'
        self.repeats = repeats
        self.label = label
        self.description = description


class SegmentGroup(object):
    def __init__(self, elements, status='M', repeats='1', label=None, description=None):
        self.elements = elements
        self.status = status
        self.mandatory = status == 'M'
        self.repeats = repeats
        self.label = label
        self.description = description

    def get(self, index):
        return self.elements[index]
