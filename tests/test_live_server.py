#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

from flask import url_for


class TestLiveServer:

    def test_server_is_alive(self, live_server):
        assert live_server._process
        assert live_server._process.is_alive()

    def test_server_url(self, live_server):
        assert live_server.url() == 'http://localhost:%d' % live_server.port
        assert live_server.url('/ping') == 'http://localhost:%d/ping' % live_server.port

    def test_server_listening(self, live_server):
        res = urlopen(live_server.url('/ping'))
        assert res.code == 200
        assert b'pong' in res.read()

    def test_url_for(self, live_server):
        assert url_for('ping', _external=True) == 'http://localhost:%s/ping' % live_server.port

    def test_set_application_server_name(self, live_server):
        assert live_server.app.config['SERVER_NAME'] == 'localhost:%d' % live_server.port

    @pytest.mark.options(server_name='example.com:5000')
    def test_rewrite_application_server_name(self, live_server):
        assert live_server.app.config['SERVER_NAME'] == 'example.com:%d' % live_server.port

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

    def test_clean_stop_live_server(self, appdir):
        pytest_cov = pytest.importorskip("pytest_cov")
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
        result_with = appdir.runpytest('-v',
                                       '--no-start-live-server',
                                       '--live-server-clean-stop',
                                       '--cov=%s' % str(appdir.tmpdir),
                                       '--cov-report=term-missing')
        result_without = appdir.runpytest('-v',
                                          '--no-start-live-server',
                                          '--no-live-server-clean-stop',
                                          '--cov=%s' % str(appdir.tmpdir),
                                          '--cov-report=term-missing')

        def _get_missing(r):
            for line in r.outlines:
                if not line.startswith('TOTAL'):
                    continue
                # Columns: Name   Stmts   Miss   Cover   Missing
                return int(line.split()[2])
            raise ValueError("Expected a TOTAL line in the cov output")

        # Read the "Missing" column (i.e. lines not covered)
        missing_with, missing_without = _get_missing(result_with), _get_missing(result_without)

        # If the clean stop worked, the single line in the view function should be covered
        assert missing_with == (missing_without - 1)

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
