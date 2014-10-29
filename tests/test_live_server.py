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
        assert live_server.url == 'http://localhost:5001'

    def test_server_listening(self, live_server):
        res = urlopen('%s/ping' % live_server.url)
        assert res.code == 200
        assert b'pong' in res.read()
