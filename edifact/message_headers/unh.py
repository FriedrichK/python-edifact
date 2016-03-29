# -*- coding: utf-8 -*-
"""Provides functionality for the UNH Message Header."""

from edifact.helpers import separate_segments, separate_components

from edifact.message_headers.una import UNA

LENGTH_OF_A_SIMPLE_ENTRY = 3
LENGTH_OF_A_NESTED_ENTRY = 4

STRUCTURE = [
    ['message_reference_number', True, 14],
    [
        'messsage_identifier',
        True,
        4,
        [
            ['message_type', True, 6],
            ['message_version_number', True, 3],
            ['message_release_number', True, 3],
            ['controlling_agency_coded', True, 3],
            ['association_assigned_code', False, 6],
            ['code_list_directory_version_number', False, 6],
            ['message_type_sub_function_identification', False, 6]
        ]
    ],
    ['common_access_reference', False, 35],
    [
        'status_of_the_transfer',
        False,
        1,
        [
            ['sequence_of_transfers', True, 2],
            ['first_and_list_transfer', False, 1]
        ]
    ],
    [
        'message_subset_identification',
        False,
        1,
        [
            ['message_subset_identification', True, 3],
            ['message_subset_version_number', False, 3],
            ['message_subset_release_number', False, 3],
            ['controlling_agency_coded', False, 3]
        ]
    ],
    [
        'message_implementaton_guideline_identification',
        False,
        1,
        [
            ['message_implementaton_guideline_identification', True, 14],
            ['message_implementaton_guideline_version_number', False, 3],
            ['message_implementaton_guideline_release_number', False, 3],
            ['controlling_agency_coded', False, 3]
        ],
    ],
    [
        'scenario_identification',
        False,
        1,
        [
            ['scenario_identification', True, 14],
            ['scenario_version_number', False, 3],
            ['scenario_release_number', False, 3],
            ['controlling_agency_coded', False, 3]
        ]
    ]
]


class UNH(object):
    """Wrapper class for UNH (Message Header)."""

    data = {}

    def __init__(self, una=None, src_string=None):
        """Constructor."""
        # UNA
        if una:
            self.una = una
        else:
            self.una = UNA()

        # Parsing
        if src_string:
            self._init_from_string(src_string)

    def _init_from_string(self, src_string):
        """Initialize from string source."""
        # Get components
        segments = separate_segments(src_string, segment_terminator=self.una.segment_terminator, release_character=self.una.release_character)
        unh_index = [i for i, x in enumerate(segments) if x.startswith('UNH')][0]
        components = separate_components(segments[unh_index], data_element_separator=self.una.data_element_separator, component_data_element_separator=self.una.component_data_element_separator, segment_terminator=self.una.segment_terminator, release_character=self.una.release_character)

        # Map comonents to standard
        self.data = process_entries(components[1:])

    def get(self, label, default=None):
        """Get a value from the nested data structure."""
        value = default
        for k, v in self.data.iteritems():
            if k == label:
                value = v
                break
            if isinstance(v, dict):
                for k2, v2 in v.iteritems():
                    if k2 == label:
                        value = v2
            if value:
                break
        return value


def process_entries(components):
    """Process top-level entries."""
    data = {}

    for index, value in enumerate(STRUCTURE):
        label = value[0]
        mandatory = value[1]

        # Raise error if mandatory elements are missing
        if index >= len(components):
            if mandatory is True:
                raise ValueError('UNH header is missing mandatory entry for {label}'.format(label=label))
            else:
                break

        # Process
        if len(value) == LENGTH_OF_A_SIMPLE_ENTRY:
            data[label] = components[index]
        elif len(value) == LENGTH_OF_A_NESTED_ENTRY:
            data[label] = process_subentries(components, index)
        else:
            raise ValueError('unexpected structure')

    return data


def process_subentries(components, parent_index):
    """Process sub-entries."""
    subentries_data = {}

    parent_label = STRUCTURE[parent_index][0]
    number_of_mandatory_subentries = STRUCTURE[parent_index][2]

    subentry_structure = STRUCTURE[parent_index][3]
    subentries = components[parent_index]

    if len(subentries) < number_of_mandatory_subentries:
        raise ValueError('entry for {0} has {1} mandatory subentries: {2} found'.format(parent_label, number_of_mandatory_subentries, len(subentries)))

    for index, value in enumerate(subentry_structure):
        if index >= len(subentries):
            break

        label = value[0]
        subentries_data[label] = subentries[index]

    return subentries_data
