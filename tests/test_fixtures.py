#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from flask import url_for


class TestFixtures:

    def test_config_access(self, config):
        assert config['SECRET_KEY'] == '42'

    def test_application_has_pushed_context(self, app):
        assert url_for('ping') == '/ping'

    def test_client(self, client):
        assert client.get(url_for('ping')).status == b'200 OK'

    def test_accept_json(self, accept_json):
        assert accept_json == [('Accept', 'application/json')]

    def test_accept_jsonp(self, accept_jsonp):
        assert accept_jsonp == [('Accept', 'application/json-p')]


class TestAppMarker:

    @pytest.mark.app(debug=False)
    def test_not_debug_app(self, app):
        assert not app.debug, 'Ensure the app not in debug mode'

    @pytest.mark.app(foo=42)
    def test_update_application_config(self, config):
        assert config['FOO'] == 42


class TestJSONResponse:

    def test_json_response(self, client, accept_json):
        res = client.get(url_for('ping'), headers=accept_json)
        assert res.json == {'ping': 'pong'}

    def test_dont_rewrite_existing_implementation(self, app, accept_json):
        class MyResponse(app.response_class):
            @property
            def json(self):
                '''What is the meaning of life, the universe and everything?'''
                return 42

        app.response_class = MyResponse
        client = app.test_client()

        res = client.get(url_for('ping'), headers=accept_json)
        assert res.json == 42


@pytest.mark.usefixtures('client_class')
class TestClientClass:

    def test_client_attribute(self):
        assert hasattr(self, 'client')
        assert self.client.get(url_for('ping')).json == {'ping': 'pong'}
