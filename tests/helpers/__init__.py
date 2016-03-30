# -*- coding: utf-8 -*-
"""Helper functions for tests."""

import os


def load_edifact_sample(name):
    """Load an EDIFACT text sample, ignoring commented lines."""
    path = os.path.dirname(__file__) + '/../data/' + name
    content = ""

    for line in open(path):
        stripped_line = line.strip()
        if not stripped_line.startswith("#"):
            content += line

    return content
