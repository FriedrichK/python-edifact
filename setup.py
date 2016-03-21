#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='python-edifact',
	version='0.1',
	description='EDIFACT toolkit for Python',
	author='Friedrich Kauder',
	author_email='fkauder@gmail.com',
	url='https://github.com/FriedrichK/python-edifact',
	packages=find_packages(exclude=('tests', 'docs')),
	setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)