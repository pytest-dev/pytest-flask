#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from flask import request, url_for


class TestFixtures:

    def test_config_access(self, config):
        assert config['SECRET_KEY'] == '42'

    def test_client(self, client):
        assert client.get(url_for('ping')).status == '200 OK'

    def test_accept_json(self, accept_json):
        assert accept_json == [('Accept', 'application/json')]

    def test_accept_jsonp(self, accept_jsonp):
        assert accept_jsonp == [('Accept', 'application/json-p')]

    def test_request_ctx(self, app, request_ctx):
        assert request_ctx.app is app

    def test_request_ctx_is_kept_around(self, client):
        client.get(url_for('index'), headers=[('X-Something', '42')])
        assert request.headers['X-Something'] == '42'


class TestJSONResponse:

    def test_json_response(self, client, accept_json):
        res = client.get(url_for('ping'), headers=accept_json)
        assert res.json == {'ping': 'pong'}

    def test_json_response_compare_to_status_code(self, client, accept_json):
        assert client.get(url_for('ping'), headers=accept_json) == 200
        assert client.get('fake-route', headers=accept_json) == 404
        assert client.get('fake-route', headers=accept_json) != '404'
        res = client.get(url_for('ping'), headers=accept_json)
        assert res == res

    def test_mismatching_eq_comparison(self, client, accept_json):
        with pytest.raises(AssertionError, match=r'Mismatch in status code'):
            assert client.get('fake-route', headers=accept_json) == 200
        with pytest.raises(AssertionError, match=r'404 NOT FOUND'):
            assert client.get('fake-route', headers=accept_json) == '200'

    def test_dont_rewrite_existing_implementation(self, app, accept_json):
        class MyResponse(app.response_class):
            @property
            def json(self):
                """What is the meaning of life, the universe and everything?"""
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
