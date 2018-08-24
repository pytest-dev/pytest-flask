#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pytest-flask
============

A set of `pytest <https://docs.pytest.org>`_ fixtures to test Flask
extensions and applications.

Features
--------

Plugin provides some fixtures to simplify app testing:

- ``client`` - an instance of ``app.test_client``,
- ``client_class`` - ``client`` fixture for class-based tests,
- ``config`` - the application config,
- ``live_server`` - runs an application in the background (useful for tests
  with `Selenium <http://www.seleniumhq.org>`_ and other headless browsers),
- ``request_ctx`` - the request context,
- ``accept_json``, ``accept_jsonp``, ``accept_any`` - accept headers
  suitable to use as parameters in ``client``.

To pass options to your application use the ``pytest.mark.options`` marker:

.. code:: python

    @pytest.mark.options(debug=False)
    def test_app(app):
      assert not app.debug, 'Ensure the app not in debug mode'

During tests execution the request context has been pushed, e.g. ``url_for``,
``session`` and other context bound objects are available without context
managers:

.. code:: python

    def test_app(client):
        assert client.get(url_for('myview')).status_code == 200

Response object has a ``json`` property to test a view that returns
a JSON response:

.. code:: python

    @api.route('/ping')
    def ping():
        return jsonify(ping='pong')

    def test_api_ping(client):
        res = client.get(url_for('api.ping'))
        assert res.json == {'ping': 'pong'}

If you want your tests done via Selenium or other headless browser use
the ``live_server`` fixture. The server’s URL can be retrieved using
the ``url_for`` function:

.. code:: python

    from flask import url_for

    @pytest.mark.usefixtures('live_server')
    class TestLiveServer:

        def test_server_is_up_and_running(self):
            res = urllib2.urlopen(url_for('index', _external=True))
            assert b'OK' in res.read()
            assert res.code == 200

Quick Start
-----------

To start using a plugin define your application fixture in ``conftest.py``:

.. code:: python

    from myapp import create_app

    @pytest.fixture
    def app():
        app = create_app()
        return app

Install the extension with dependencies and run your test suite:

.. code:: bash

    $ pip install pytest-flask
    $ py.test

Documentation
-------------

The latest documentation is available at
http://pytest-flask.readthedocs.org/en/latest/.

Contributing
------------

Don’t hesitate to create a `GitHub issue
<https://github.com/vitalk/pytest-flask/issues>`_ for any **bug** or
**suggestion**.

"""
import io
import os
import re
from setuptools import setup
from setuptools import find_packages


def read(*parts):
    """Reads the content of the file located at path created from *parts*."""
    try:
        return io.open(os.path.join(*parts), 'r', encoding='utf-8').read()
    except IOError:
        return ''


requirements = read('requirements', 'main.txt').splitlines() + ['pytest']
tests_require = []

extras_require = {
    'docs': read('requirements', 'docs.txt').splitlines(),
    'tests': tests_require
}


setup(
    name='pytest-flask',

    # Versions should comply with PEP440, and automatically obtained from tags
    # thanks to setuptools_scm
    use_scm_version={"write_to": "pytest_flask/_version.py"},
    setup_requires=["setuptools-scm"],

    author='Vital Kudzelka',
    author_email='vital.kudzelka@gmail.com',

    url='https://github.com/vitalk/pytest-flask',
    project_urls={
        "Source": "https://github.com/pytest-dev/pytest-flask",
        "Tracker": "https://github.com/pytest-dev/pytest-flask/issues",
    },
    description='A set of py.test fixtures to test Flask applications.',
    long_description=__doc__,
    license='MIT',

    packages=find_packages(exclude=['docs', 'tests']),
    zip_safe=False,
    platforms='any',
    install_requires=requirements,
    tests_require=tests_require,
    extras_require=extras_require,

    keywords='pytest flask testing',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    # The following makes a plugin available to pytest
    entry_points={
        'pytest11': [
            'flask = pytest_flask.plugin',
        ]
    },
)
