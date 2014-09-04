#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    A py.test plugin which helps testing Flask applications.

    :copyright: (c) by Vital Kudzelka
    :license: MIT
"""
import pytest

from .fixtures import (
    client, config, accept_json, accept_jsonp
)


@pytest.fixture(autouse=True)
def _push_application_context(request):
    """During tests execution application has pushed context, e.g. `url_for`,
    `session`, etc. can be used in tests as is::

        def test_app(app, client):
            assert client.get(url_for('myview')).status_code == 200

    """
    if 'app' not in request.fixturenames:
        return

    app = request.getfuncargvalue('app')
    ctx = app.test_request_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)


@pytest.fixture(autouse=True)
def _configure_application(request):
    """Use `pytest.mark.app` decorator to pass options to your application
    factory::

        @pytest.mark.app(debug=False)
        def test_something(app):
            assert not app.debug, 'the application works not in debug mode!'

    """
    if 'app' not in request.fixturenames:
        return

    app = request.getfuncargvalue('app')
    options = request.keywords.get('app', None)
    if options:
        for key, value in options.kwargs.items():
            app.config[key.upper()] = value


def pytest_configure(config):
    config.addinivalue_line(
        'markers',
        'app(options): pass options to your application factory')
