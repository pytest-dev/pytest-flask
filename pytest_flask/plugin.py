#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    A py.test plugin which helps testing Flask applications.

    :copyright: (c) by Vital Kudzelka
    :license: MIT
"""
import pytest

from flask import json
from werkzeug import cached_property

from .fixtures import (
    client, config, accept_json, accept_jsonp, accept_any, accept_mimetype,
    client_class, live_server, request_ctx
)


class JSONResponse(object):
    """Mixin with testing helper methods for JSON responses."""

    @cached_property
    def json(self):
        """Try to deserialize response data (a string containing a valid JSON
        document) to a Python object by passing it to the underlying
        :mod:`flask.json` module.
        """
        return json.loads(self.data)


def _make_test_response_class(response_class):
    """Extends the response class with special attribute to test JSON
    responses. Don't override user-defined `json` attribute if any.

    :param response_class: An original response class.
    """
    if 'json' in response_class.__dict__:
        return response_class

    return type(str(JSONResponse), (response_class, JSONResponse), {})


@pytest.fixture(autouse=True)
def _monkeypatch_response_class(request, monkeypatch):
    """Set custom response class before test suite and restore the original
    after. Custom response has `json` property to easily test JSON responses::

        @app.route('/ping')
        def ping():
            return jsonify(ping='pong')

        def test_json(client):
            res = client.get(url_for('ping'))
            assert res.json == {'ping': 'pong'}

    """
    if 'app' not in request.fixturenames:
        return

    app = request.getfuncargvalue('app')
    monkeypatch.setattr(app, 'response_class',
                        _make_test_response_class(app.response_class))


@pytest.fixture(autouse=True)
def _push_request_context(request):
    """During tests execution request context has been pushed, e.g. `url_for`,
    `session`, etc. can be used in tests as is::

        def test_app(app, client):
            assert client.get(url_for('myview')).status_code == 200

    """
    if 'app' not in request.fixturenames:
        return

    app = request.getfuncargvalue('app')

    # Get application bound to the live server if ``live_server`` fixture
    # is applyed. Live server application has an explicit ``SERVER_NAME``,
    # so ``url_for`` function generates a complete URL for endpoint which
    # includes application port as well.
    if 'live_server' in request.fixturenames:
        app = request.getfuncargvalue('live_server').app

    ctx = app.test_request_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)


@pytest.fixture(autouse=True)
def _configure_application(request, monkeypatch):
    """Use `pytest.mark.options` decorator to pass options to your application
    factory::

        @pytest.mark.options(debug=False)
        def test_something(app):
            assert not app.debug, 'the application works not in debug mode!'

    """
    if 'app' not in request.fixturenames:
        return

    app = request.getfuncargvalue('app')
    options = request.keywords.get('options')
    if options is not None:
        for key, value in options.kwargs.items():
            monkeypatch.setitem(app.config, key.upper(), value)


def pytest_addoption(parser):
    group = parser.getgroup('flask')
    group.addoption('--start-live-server',
                    action="store_true", dest="start_live_server", default=True,
                    help="start server automatically when live_server "
                         "fixture is applyed (enabled by default).")
    group.addoption('--no-start-live-server',
                    action="store_false", dest="start_live_server",
                    help="don't start server automatically when live_server "
                         "fixture is applyed.")


def pytest_configure(config):
    config.addinivalue_line(
        'markers',
        'app(options): pass options to your application factory')
