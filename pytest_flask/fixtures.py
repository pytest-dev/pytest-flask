#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import pytest
import multiprocessing
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen


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
        self.start()

    def start(self):
        """Start application in a separate process."""
        worker = lambda app, port: app.run(port=port, use_reloader=False)
        self._process = multiprocessing.Process(
            target=worker,
            args=(self.app, self.port)
        )
        self._process.start()

        # We must wait for the server to start listening with a maximum
        # timeout of 5 seconds.
        timeout = 5
        while timeout > 0:
            time.sleep(1)
            try:
                urlopen(self.url)
                timeout = 0
            except:
                timeout -= 1

    @property
    def url(self):
        """Returns the url of the test server."""
        return 'http://localhost:%s' % self.port

    def stop(self):
        """Stop application process."""
        if self._process:
            self._process.terminate()

    def __repr__(self):
        return '<LiveServer listening at %s>' % self.url


@pytest.fixture(scope='session')
def live_server(request, app):
    """Run application in a separate process."""
    port = app.config.get('LIVESERVER_PORT', 5001)
    server = LiveServer(app, port)
    request.addfinalizer(server.stop)
    return server


@pytest.fixture
def config(app):
    """An application config."""
    return app.config


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
