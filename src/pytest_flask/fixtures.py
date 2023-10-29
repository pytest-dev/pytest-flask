#!/usr/bin/env python
import socket
from typing import Any
from typing import cast
from typing import Generator

import pytest
from flask import Flask as _FlaskApp
from flask.config import Config as _FlaskAppConfig
from flask.testing import FlaskClient as _FlaskTestClient
from pytest import Config as _PytestConfig
from pytest import FixtureRequest as _PytestFixtureRequest

from ._internal import _determine_scope
from ._internal import _make_accept_header
from ._internal import _rewrite_server_name
from .live_server import LiveServer


@pytest.fixture
def client(app: _FlaskApp) -> Generator[_FlaskTestClient, Any, Any]:
    """A Flask test client. An instance of :class:`flask.testing.TestClient`
    by default.
    """
    with app.test_client() as client:
        yield client


@pytest.fixture
def client_class(request: _PytestFixtureRequest, client: _FlaskTestClient) -> None:
    """Uses to set a ``client`` class attribute to current Flask test client::

    @pytest.mark.usefixtures('client_class')
    class TestView:

        def login(self, email, password):
            credentials = {'email': email, 'password': password}
            return self.client.post(url_for('login'), data=credentials)

        def test_login(self):
            assert self.login('foo@example.com', 'pass').status_code == 200

    """
    if request.cls is not None:
        request.cls.client = client


@pytest.fixture(scope=_determine_scope)  # type: ignore[arg-type]
def live_server(
    request: _PytestFixtureRequest, app: _FlaskApp, pytestconfig: _PytestConfig
) -> Generator[LiveServer, Any, Any]:  # pragma: no cover
    """Run application in a separate process.

    When the ``live_server`` fixture is applied, the ``url_for`` function
    works as expected::

        def test_server_is_up_and_running(live_server):
            index_url = url_for('index', _external=True)
            assert index_url == 'http://localhost:5000/'

            res = urllib2.urlopen(index_url)
            assert res.code == 200

    """
    # Set or get a port
    port = app.config.get("LIVESERVER_PORT", None)
    if not port:
        port = pytestconfig.getvalue("live_server_port")

    if port == 0:
        # Bind to an open port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 0))
        port = s.getsockname()[1]
        s.close()

    host = cast(str, pytestconfig.getvalue("live_server_host"))

    # Explicitly set application ``SERVER_NAME`` for test suite
    original_server_name = app.config["SERVER_NAME"] or "localhost.localdomain"
    final_server_name = _rewrite_server_name(original_server_name, str(port))
    app.config["SERVER_NAME"] = final_server_name

    wait = cast(int, request.config.getvalue("live_server_wait"))
    clean_stop = cast(bool, request.config.getvalue("live_server_clean_stop"))

    server = LiveServer(app, host, port, wait, clean_stop)
    if request.config.getvalue("start_live_server"):
        server.start()

    request.addfinalizer(server.stop)

    yield server

    if original_server_name is not None:
        app.config["SERVER_NAME"] = original_server_name


@pytest.fixture
def config(app: _FlaskApp) -> _FlaskAppConfig:
    """An application config."""
    return app.config


@pytest.fixture(params=["application/json", "text/html"])
def mimetype(request) -> str:
    return request.param


@pytest.fixture
def accept_mimetype(mimetype):
    return _make_accept_header(mimetype)


@pytest.fixture
def accept_json(request):
    return _make_accept_header("application/json")


@pytest.fixture
def accept_jsonp():
    return _make_accept_header("application/json-p")


@pytest.fixture(params=["*", "*/*"])
def accept_any(request):
    return _make_accept_header(request.param)
