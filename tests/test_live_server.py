#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import pytest
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

from flask import url_for


pytestmark = pytest.mark.skipif(not hasattr(os, 'fork'), reason='needs fork')


class TestLiveServer:

    def test_server_is_alive(self, live_server):
        assert live_server._process
        assert live_server._process.is_alive()

    def test_server_url(self, live_server):
        assert live_server.url() == 'http://localhost:%d' % live_server.port
        assert live_server.url('/ping') == \
            'http://localhost:%d/ping' % live_server.port

    def test_server_listening(self, live_server):
        res = urlopen(live_server.url('/ping'))
        assert res.code == 200
        assert b'pong' in res.read()

    def test_url_for(self, live_server):
        assert url_for('ping', _external=True) == \
            'http://localhost:%s/ping' % live_server.port

    def test_set_application_server_name(self, live_server):
        assert live_server.app.config['SERVER_NAME'] == \
            'localhost:%d' % live_server.port

    @pytest.mark.options(server_name='example.com:5000')
    def test_rewrite_application_server_name(self, live_server):
        assert live_server.app.config['SERVER_NAME'] == \
            'example.com:%d' % live_server.port

    def test_prevent_starting_live_server(self, appdir):
        appdir.create_test_module('''
            import pytest

            def test_a(live_server):
                assert live_server._process is None
        ''')

        result = appdir.runpytest('-v', '--no-start-live-server')
        result.stdout.fnmatch_lines(['*PASSED*'])
        assert result.ret == 0

    def test_start_live_server(self, appdir):
        appdir.create_test_module('''
            import pytest

            def test_a(live_server):
                assert live_server._process
                assert live_server._process.is_alive()
        ''')
        result = appdir.runpytest('-v', '--start-live-server')
        result.stdout.fnmatch_lines(['*PASSED*'])
        assert result.ret == 0

    @pytest.mark.parametrize('clean_stop', [True, False])
    def test_clean_stop_live_server(self, appdir, monkeypatch, clean_stop):
        """Ensure the fixture is trying to cleanly stop the server.

        Because this is tricky to test, we are checking that the _stop_cleanly() internal
        function was called and reported success.
        """
        from pytest_flask.fixtures import LiveServer

        original_stop_cleanly_func = LiveServer._stop_cleanly

        stop_cleanly_result = []

        def mocked_stop_cleanly(*args, **kwargs):
            result = original_stop_cleanly_func(*args, **kwargs)
            stop_cleanly_result.append(result)
            return result

        monkeypatch.setattr(LiveServer, '_stop_cleanly', mocked_stop_cleanly)

        appdir.create_test_module('''
            import pytest
            try:
                from urllib2 import urlopen
            except ImportError:
                from urllib.request import urlopen

            from flask import url_for

            def test_a(live_server):
                @live_server.app.route('/')
                def index():
                    return 'got it', 200

                live_server.start()

                res = urlopen(url_for('index', _external=True))
                assert res.code == 200
                assert b'got it' in res.read()
        ''')
        args = [] if clean_stop else ['--no-live-server-clean-stop']
        result = appdir.runpytest_inprocess('-v', '--no-start-live-server',
                                            *args)
        result.stdout.fnmatch_lines('*1 passed*')
        if clean_stop:
            assert stop_cleanly_result == [True]
        else:
            assert stop_cleanly_result == []

    def test_add_endpoint_to_live_server(self, appdir):
        appdir.create_test_module('''
            import pytest
            try:
                from urllib2 import urlopen
            except ImportError:
                from urllib.request import urlopen

            from flask import url_for

            def test_a(live_server):
                @live_server.app.route('/new-endpoint')
                def new_endpoint():
                    return 'got it', 200

                live_server.start()

                res = urlopen(url_for('new_endpoint', _external=True))
                assert res.code == 200
                assert b'got it' in res.read()
        ''')
        result = appdir.runpytest('-v', '--no-start-live-server')
        result.stdout.fnmatch_lines(['*PASSED*'])
        assert result.ret == 0

    def test_concurrent_requests_to_live_server(self, appdir):
        appdir.create_test_module('''
            import pytest
            try:
                from urllib2 import urlopen
            except ImportError:
                from urllib.request import urlopen

            from flask import url_for

            def test_concurrent_requests(live_server):
                @live_server.app.route('/one')
                def one():
                    res = urlopen(url_for('two', _external=True))
                    return res.read()

                @live_server.app.route('/two')
                def two():
                    return '42'

                live_server.start()

                res = urlopen(url_for('one', _external=True))
                assert res.code == 200
                assert b'42' in res.read()
        ''')
        result = appdir.runpytest('-v', '--no-start-live-server')
        result.stdout.fnmatch_lines(['*PASSED*'])
        assert result.ret == 0

    @pytest.mark.parametrize('port', [5000, 5001])
    def test_live_server_fixed_port(self, port, appdir):
        appdir.create_test_module('''
            import pytest

            def test_port(live_server):
                assert live_server.port == %d
        ''' % port)
        result = appdir.runpytest('-v', '--live-server-port', str(port))
        result.stdout.fnmatch_lines(['*PASSED*'])
        assert result.ret == 0

    @pytest.mark.parametrize('host', ['127.0.0.1', '0.0.0.0'])
    def test_live_server_fixed_host(self, host, appdir):
        appdir.create_test_module('''
            import pytest

            def test_port(live_server):
                assert live_server.host == '%s'
        ''' % host)
        result = appdir.runpytest('-v', '--live-server-host', str(host))
        result.stdout.fnmatch_lines(['*PASSED*'])
        assert result.ret == 0
