#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import multiprocessing
import pytest
import socket

try:
    from urllib.request import urlopen
    from shutil import which
except ImportError:
    from urllib2 import urlopen
    from distutils.spawn import find_executable as which

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
                assert self.login('vital@foo.com', 'pass').status_code == 200

    """
    if request.cls is not None:
        request.cls.client = client


def _find_unused_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


class LiveServerBase(object):

    def __init__(self, app, monkeypatch, port=None):
        self.app = app
        self.port = port or _find_unused_port()
        self._process = None
        self.monkeypatch = monkeypatch

    def start(self):
        # Explicitly set application ``SERVER_NAME`` for test suite
        # and restore original value on test teardown.
        server_name = self.app.config['SERVER_NAME'] or '127.0.0.1'
        self.monkeypatch.setitem(
            self.app.config, 'SERVER_NAME',
            _rewrite_server_name(server_name, str(self.port)))

    def _wait_for_server(self):
        # We must wait for the server to start listening with a maximum
        # timeout of 5 seconds.
        timeout = 5
        while timeout > 0:
            time.sleep(1)
            try:
                urlopen(self.url())
                timeout = 0
            except:
                timeout -= 1

    def url(self, url=''):
        """Returns the complete url based on server options."""
        return 'http://127.0.0.1:%d%s' % (self.port, url)

    def __repr__(self):
        return '<%s listening at %s>' % (
            self.__class__.__name,
            self.url(),
        )


class LiveServerMultiprocess(LiveServerBase):
    """The helper class uses this to manage live server.
    Handles creation and stopping application in a separate process.

    :param app: The application to run.
    :param port: The port to run application.
    """

    def start(self):
        """Start application in a separate process."""
        def worker(app, port):
            return app.run(port=port, use_reloader=False)
        super(LiveServerMultiprocess, self).start()

        self._process = multiprocessing.Process(
            target=worker,
            args=(self.app, self.port)
        )
        self._process.start()
        self._wait_for_server()

    def stop(self):
        """Stop application process."""
        if self._process:
            self._process.terminate()

try:
    import pytest_services  # noqa

    class LiveServerSubprocess(LiveServerBase):
        """The helper class uses this to manage live server.
        Handles creation and stopping application in a subprocess
        using Popen. Use this if you need more explicit separation
        between processes.

        :param app: The application to run.
        :param port: The port to run application.
        """
        def __init__(self, app, monkeypatch, watcher_getter, port=None):
            self.app = app
            self.port = port or _find_unused_port()
            self._process = None
            self.monkeypatch = monkeypatch
            self.watcher_getter = watcher_getter

        def start(self, **kwargs):
            """
            Start application in a separate process.

            To add environment variables to the process, simply do:
            live_server_subprocess.start(
                watcher_getter_kwargs={'env': {'MYENV': '1'}})
            """
            def worker(app, port):
                return app.run(port=port, use_reloader=False)
            super(LiveServerSubprocess, self).start()

            self._process = self.watcher_getter(
                name='flask',
                arguments=['run', '--port', str(self.port)],
                checker=lambda: which('flask'),
                kwargs=kwargs.get('watcher_getter_kwargs', {}))
            self._wait_for_server()

        def stop(self):
            """Stop application process."""
            if self._process:
                self._process.terminate()

    @pytest.yield_fixture(scope='function')
    def live_server_subprocess(request, app, monkeypatch, watcher_getter):
        """Run application in a subprocess. Use this if you need more explicit
        separation of processes. Uses os.fork().
        Requires flask >= 0.11 and the pytest-services plugin.

        When the ``live_server_subprocess`` fixture is applyed,
        the ``url_for`` function works as expected::

            def test_server_is_up_and_running(live_server_subprocess):
                index_url = url_for('index', _external=True)
                assert index_url == 'http://127.0.0.1:5000/'

                res = urllib2.urlopen(index_url)
                assert res.code == 200
        """

        server = LiveServerSubprocess(app, monkeypatch=monkeypatch)
        if request.config.getvalue('start_live_server'):
            server.start()
        yield server
        server.stop()

except ImportError:
    pass


def _rewrite_server_name(server_name, new_port):
    """Rewrite server port in ``server_name`` with ``new_port`` value."""
    sep = ':'
    if sep in server_name:
        server_name, port = server_name.split(sep, 1)
    return sep.join((server_name, new_port))


@pytest.yield_fixture(scope='function')
def live_server(request, app, monkeypatch):
    """Run application in a separate process.

    When the ``live_server`` fixture is applyed, the ``url_for`` function
    works as expected::

        def test_server_is_up_and_running(live_server):
            index_url = url_for('index', _external=True)
            assert index_url == 'http://127.0.0.1:5000/'

            res = urllib2.urlopen(index_url)
            assert res.code == 200

    """

    server = LiveServerMultiprocess(app, monkeypatch=monkeypatch)
    if request.config.getvalue('start_live_server'):
        server.start()
    yield server
    server.stop()


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
