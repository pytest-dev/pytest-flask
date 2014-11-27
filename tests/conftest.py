#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from flask import Flask, jsonify


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '42'

    @app.route('/')
    def index():
        return app.response_class('OK')

    @app.route('/ping')
    def ping():
        return jsonify(ping='pong')

    return app
