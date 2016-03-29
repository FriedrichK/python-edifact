# -*- coding: utf-8 -*-
"""This module provides the base for segment wrappers."""

import six


class Composite(object):
    """Part of a segment."""

    _content = None

    def __init__(self, index=0, max_length=3, required=False):
        """Constructor."""
        self.index = index
        self.max_length = max_length
        self.required = required

    @property
    def content(self):
        """Get value."""
        return self._content

    @content.setter
    def content(self, content):
        """Set content."""
        if len(content) > self.max_length:
            raise ValueError('trying to set content {0} for composite with maximum length {1}'.format(content, unicode(self.max_length)))
        self._content = content

    def __str__(self):
        """Return value."""
        return self.content or u''


class SegmentMeta(type):
    """Meta class for segments."""

    def __new__(cls, name, bases, attrs):
        """Create class."""
        cleanup = []

        # composites
        composites = {}
        for key, value in attrs.iteritems():
            if isinstance(value, Composite):
                composites[key] = value
                cleanup.append(key)
        attrs['_composites'] = composites

        # cleanup
        for key in cleanup:
            del attrs[key]

        # Meta
        attrs['_meta'] = attrs.pop('Meta', None)

        return super(SegmentMeta, cls).__new__(cls, name, bases, attrs)


class Segment(six.with_metaclass(SegmentMeta)):
    """Base class for segments."""

    def __init__(self, una, **kwargs):
        """Constructor."""
        self.una = una

        for key, value in kwargs.iteritems():
            if key not in self._composites:
                raise IndexError('composite {0} not found'.format(key,))
            self._composites[key].content = value

    def __str__(self):
        """Return the string representation of this segment."""
        ordered_composites = [unicode(composite) for composite in sorted(self._composites.values(), key=lambda x: x.index)]
        return ''.join((
            self._meta.identifier,  # segment tag
            self.una.data_element_separator,  # segment tag separator
            self.una.component_data_element_separator.join(ordered_composites),  # composites
            self.una.segment_terminator,  # terminator
        ))
