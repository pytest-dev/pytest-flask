#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest


@pytest.yield_fixture
def client(app):
    """A Flask test client. An instance of :class:`flask.testing.TestClient`
    by default.
    """
    with app.test_client() as client:
        yield client


@pytest.fixture
def config(app):
    """An application config."""
    return app.config
