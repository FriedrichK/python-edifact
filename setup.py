#!/usr/bin/env python

import sys
import os

from setuptools import setup, find_packages


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'tests')))

setup(
    name='python-edifact',
    version='0.1',
    description='EDIFACT toolkit for Python',
    author='Friedrich Kauder',
    author_email='fkauder@gmail.com',
    url='https://github.com/FriedrichK/python-edifact',
    packages=find_packages(exclude=('tests', 'docs')),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
