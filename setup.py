#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    pytest-flask
    ~~~~~~~~~~~~

    A collection of py.test fixtures to test Flask applications.

    :copyright: (c) by Vital Kudzelka
"""
from setuptools import setup
from setuptools import find_packages


version = "0.3.0"


def get_file(filename):
    """Returns file content line by line."""
    try:
        with open(filename, 'r') as f:
            rv = f.readlines()
    except IOError:
        rv = []
    return rv


def get_long_description():
    readme = get_file('README')
    return ''.join(readme)


setup(
    name='pytest-flask',

    # Versions should comply with PEP440. For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version=version,

    author='Vital Kudzelka',
    author_email='vital.kudzelka@gmail.com',

    url='https://github.com/vitalk/pytest-flask',
    description='A collection of py.test fixtures to test Flask applications.',
    long_description=get_long_description(),
    license='MIT',

    packages=find_packages(exclude=['docs', 'tests']),
    zip_safe=False,
    platforms='any',
    install_requires=get_file('requirements.txt'),
    tests_require=[],

    keywords='pytest flask testing',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],

    # The following makes a plugin available to pytest
    entry_points = {
        'pytest11': [
            'flask = pytest_flask.plugin',
        ]
    },
)
