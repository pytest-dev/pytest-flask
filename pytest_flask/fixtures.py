#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import multiprocessing
import pytest
import socket
import logging

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

try:
    # Python 2
    from Queue import Empty
except ImportError:
    # Python 3
    from queue import Empty

from flask import _request_ctx_stack


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
                assert self.login('vital@example.com', 'pass').status_code == 200

    """
    if request.cls is not None:
        request.cls.client = client


class LogCapture(logging.Handler):
    """
    Helper class to capture logs of werkzeug and wait for a specific
    log message to confirm the server was started.
    """

    def __init__(self, logger, wait_for, queue, level=logging.NOTSET):
        super(LogCapture, self).__init__(level=level)
        self.logger_name = logger
        self.logger = logging.getLogger(self.logger_name)
        self.level = level
        self.wait_for = wait_for
        self.queue = queue

    def emit(self, record):
        if self.wait_for in record.getMessage():
            self.queue.put(1)

    def __enter__(self):
        self.logger.addHandler(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.removeHandler(self)


class LiveServer(object):
    """The helper class uses to manage live server. Handles creation and
    stopping application in a separate process.

    :param app: The application to run.
    :param port: The port to run application.
    """

    def __init__(self, app, port):
        self.app = app
        self.port = port
        self._process = None
        self._queue = None

    def start(self):
        """Start application in a separate process."""
        def worker(app, port, queue):
            with LogCapture('werkzeug', ' * Running on ', queue, logging.INFO):
                app.run(port=port, use_reloader=False)
        self._queue = multiprocessing.Queue()
        self._process = multiprocessing.Process(
            target=worker,
            args=(self.app, self.port, self._queue)
        )
        self._process.start()

        # We must wait for the server to start listening with a maximum
        # timeout of 5 seconds.
        timeout = 5
        while timeout > 0:
            try:
                # It will return 1 in less than a second or wait 1 second
                self._queue.get(True, 1)
            except Empty:
                pass  # Ignore that exception
            try:
                urlopen(self.url())
                timeout = 0
            except:
                timeout -= 1

    def url(self, url=''):
        """Returns the complete url based on server options."""
        return 'http://localhost:%d%s' % (self.port, url)

    def stop(self):
        """Stop application process."""
        if self._process:
            self._process.terminate()

    def __repr__(self):
        return '<LiveServer listening at %s>' % self.url()


def _rewrite_server_name(server_name, new_port):
    """Rewrite server port in ``server_name`` with ``new_port`` value."""
    sep = ':'
    if sep in server_name:
        server_name, port = server_name.split(sep, 1)
    return sep.join((server_name, new_port))


@pytest.fixture(scope='function')
def live_server(request, app, monkeypatch):
    """Run application in a separate process.

    When the ``live_server`` fixture is applyed, the ``url_for`` function
    works as expected::

        def test_server_is_up_and_running(live_server):
            index_url = url_for('index', _external=True)
            assert index_url == 'http://localhost:5000/'

            res = urllib2.urlopen(index_url)
            assert res.code == 200

    """
    # Bind to an open port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()

    # Explicitly set application ``SERVER_NAME`` for test suite
    # and restore original value on test teardown.
    server_name = app.config['SERVER_NAME'] or 'localhost'
    monkeypatch.setitem(app.config, 'SERVER_NAME',
                        _rewrite_server_name(server_name, str(port)))

    server = LiveServer(app, port)
    if request.config.getvalue('start_live_server'):
        server.start()

    request.addfinalizer(server.stop)
    return server


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


@pytest.fixture(params=['application/json', 'text/html'])
def mimetype(request):
    return request.param


@pytest.fixture
def accept_mimetype(mimetype):
    return [('Accept', mimetype)]


@pytest.fixture
def accept_json(request):
    return accept_mimetype('application/json')


@pytest.fixture
def accept_jsonp():
    return accept_mimetype('application/json-p')


@pytest.fixture(params=['*', '*/*'])
def accept_any(request):
    return accept_mimetype(request.param)
