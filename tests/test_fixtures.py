#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from flask import request, url_for, Flask


class TestFixtures:
    def test_config_access(self, config):
        assert config['SECRET_KEY'] == '42'

    def test_client(self, app, client):
        with app.test_request_context():
            assert client.get(url_for('ping')).status == '200 OK'

    def test_accept_json(self, accept_json):
        assert accept_json == [('Accept', 'application/json')]

    def test_accept_jsonp(self, accept_jsonp):
        assert accept_jsonp == [('Accept', 'application/json-p')]


class TestClientTeardown:
    @staticmethod
    @pytest.fixture
    def app():
        """App, that registers if request teardown was happened."""
        app = Flask(__name__)
        app.route('/spam')(lambda: 'eggs')

        app.teardown_happened = False

        @app.teardown_request
        def teardown(*_, **__):
            app.teardown_happened = True

        return app

    def test_client_teardown(self, app, client):
        """Request teardown happens before test teardown."""
        # app, client = app_and_client

        assert client.get('/spam').status_code == 200
        assert app.teardown_happened


class TestJSONResponse:

    def test_json_response(self, app, client, accept_json):
        with app.test_request_context():
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
        with app.test_request_context():
            res = client.get(url_for('ping'), headers=accept_json)
        assert res.json == 42


@pytest.mark.usefixtures('client_class')
class TestClientClass:

    def test_client_attribute(self, app):
        assert hasattr(self, 'client')
        with app.test_request_context():
            assert self.client.get(url_for('ping')).json == {'ping': 'pong'}
