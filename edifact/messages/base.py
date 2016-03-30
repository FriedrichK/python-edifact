# -*- coding: utf-8 -*-
"""This module provides the base for message wrappers."""

import os

import xml.etree.ElementTree as ET
import six

from edifact.helpers import separate_segments, separate_components, validate_anchor_segments


class MessageMeta(type):
    """Meta class for segments."""

    def __new__(cls, name, bases, attrs):
        """Create class."""
        if 'Meta' in attrs:
            attrs = generate_structure(attrs)
        # Super
        return super(MessageMeta, cls).__new__(cls, name, bases, attrs)


def generate_structure(attrs):
    xml_spec = get_xml_spec(attrs['Meta'])

    attrs['elements'] = []

    for child in xml_spec.getroot():
        attrs['elements'].append(process_element(child))

    print attrs['elements']

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

        for segment in segments:
            print segment


# Just for now
class PlaceholderSegment(object):
    def __init__(self, tag, status='M', repeats='1'):
        self.tag = tag
        self.status = status
        self.repeats = repeats


class SegmentGroup(object):
    def __init__(self, elements, status='M', repeats='1'):
        self.elements = elements
        self.status = status
        self.repeats = repeats
