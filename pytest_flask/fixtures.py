#!/usr/bin/env python
import functools
import logging
import multiprocessing
import os
import signal
import socket
import time
import warnings

import pytest
from flask import _request_ctx_stack


def deprecated(reason):
    """Decorator which can be used to mark function or method as deprecated.
    It will result a warning being emmitted when the function is called.
    """

    def decorator(func):
        @functools.wraps(func)
        def deprecated_call(*args, **kwargs):
            warnings.simplefilter("always", DeprecationWarning)
            warnings.warn(reason, DeprecationWarning, stacklevel=2)
            warnings.simplefilter("default", DeprecationWarning)
            return func(*args, **kwargs)

        return deprecated_call

    return decorator


@pytest.yield_fixture
def client(app):
    """A Flask test client. An instance of :class:`flask.testing.TestClient`
    by default.
    """
    with app.test_client() as client:
        yield client


@pytest.fixture
def client_class(request, client):
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


class LiveServer:
    """The helper class used to manage a live server. Handles creation and
    stopping application in a separate process.

    :param app: The application to run.
    :param host: The host where to listen (default localhost).
    :param port: The port to run application.
    :param wait: The timeout after which test case is aborted if
                 application is not started.
    """

    def __init__(self, app, host, port, wait, clean_stop=False):
        self.app = app
        self.port = port
        self.host = host
        self.wait = wait
        self.clean_stop = clean_stop
        self._process = None

    def start(self):
        """Start application in a separate process."""

        def worker(app, host, port):
            app.run(host=host, port=port, use_reloader=False, threaded=True)

        self._process = multiprocessing.Process(
            target=worker, args=(self.app, self.host, self.port)
        )
        self._process.daemon = True
        self._process.start()

        keep_trying = True
        start_time = time.time()
        while keep_trying:
            elapsed_time = time.time() - start_time
            if elapsed_time > self.wait:
                pytest.fail(
                    "Failed to start the server after {!s} "
                    "seconds.".format(self.wait)
                )
            if self._is_ready():
                keep_trying = False

    def _is_ready(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.host, self.port))
        except socket.error:
            ret = False
        else:
            ret = True
        finally:
            sock.close()
        return ret

    @deprecated(
        reason=(
            'The "live_server.url" method is deprecated and will '
            "be removed in the future. Please use "
            'the "flask.url_for" function instead.',
        )
    )
    def url(self, url=""):
        """Returns the complete url based on server options."""
        return "http://{host!s}:{port!s}{url!s}".format(
            host=self.host, port=self.port, url=url
        )

    def stop(self):
        """Stop application process."""
        if self._process:
            if self.clean_stop and self._stop_cleanly():
                return
            if self._process.is_alive():
                # If it's still alive, kill it
                self._process.terminate()

    def _stop_cleanly(self, timeout=5):
        """Attempts to stop the server cleanly by sending a SIGINT signal and waiting for
        ``timeout`` seconds.

        :return: True if the server was cleanly stopped, False otherwise.
        """
        try:
            os.kill(self._process.pid, signal.SIGINT)
            self._process.join(timeout)
            return True
        except Exception as ex:
            logging.error("Failed to join the live server process: %r", ex)
            return False

    def __repr__(self):
        return "<LiveServer listening at %s>" % self.url()


def _rewrite_server_name(server_name, new_port):
    """Rewrite server port in ``server_name`` with ``new_port`` value."""
    sep = ":"
    if sep in server_name:
        server_name, port = server_name.split(sep, 1)
    return sep.join((server_name, new_port))


def determine_scope(*, fixture_name, config):
    return config.getini("live_server_scope")


@pytest.fixture(scope=determine_scope)
def live_server(request, app, pytestconfig):
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

    host = pytestconfig.getvalue("live_server_host")

    # Explicitly set application ``SERVER_NAME`` for test suite
    original_server_name = app.config["SERVER_NAME"] or "localhost"
    final_server_name = _rewrite_server_name(original_server_name, str(port))
    app.config["SERVER_NAME"] = final_server_name

    wait = request.config.getvalue("live_server_wait")
    clean_stop = request.config.getvalue("live_server_clean_stop")
    server = LiveServer(app, host, port, wait, clean_stop)
    if request.config.getvalue("start_live_server"):
        server.start()

    request.addfinalizer(server.stop)
    yield server

    if original_server_name is not None:
        app.config["SERVER_NAME"] = original_server_name


@pytest.fixture
def config(app):
    """An application config."""
    return app.config


@pytest.fixture
def request_ctx(app):
    """The request context which contains all request relevant information,
    e.g. `session`, `g`, `flashes`, etc.
    """
    return _request_ctx_stack.top


@pytest.fixture(params=["application/json", "text/html"])
def mimetype(request):
    return request.param


def _make_accept_header(mimetype):
    return [("Accept", mimetype)]


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
