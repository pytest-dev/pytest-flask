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
        assert live_server.url() == 'http://localhost:5001'
        assert live_server.url('/ping') == 'http://localhost:5001/ping'

    def test_server_listening(self, live_server):
        res = urlopen(live_server.url('/ping'))
        assert res.code == 200
        assert b'pong' in res.read()

    @pytest.mark.app(liveserver_port=5042)
    def test_custom_server_port(self, live_server):
        assert live_server.url() == 'http://localhost:5042'
