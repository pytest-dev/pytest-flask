import pytest
from flask import request
from flask import url_for


class TestFixtures:
    def test_config_access(self, config):
        assert config["SECRET_KEY"] == "42"

    def test_client(self, client):
        assert client.get(url_for("ping")).status == "200 OK"

    def test_accept_json(self, accept_json):
        assert accept_json == [("Accept", "application/json")]

    def test_accept_jsonp(self, accept_jsonp):
        assert accept_jsonp == [("Accept", "application/json-p")]

    def test_request_ctx(self, app, request_ctx):
        assert request_ctx.app is app

    def test_request_ctx_is_kept_around(self, client):
        res = client.get(url_for("index"), headers=[("X-Something", "42")])
        """In werkzeug 2.0.0 the test Client provides a new attribute 'request'
        in the response class wich holds a reference to the request object that
        produced the respective response, making instrospection easier"""
        try:
            assert res.request.headers["X-Something"] == "42"
        except AttributeError:
            """This is the conventional (pre 2.0.0) way of reaching the
            request object, using flask.request global."""
            assert request.headers["X-Something"] == "42"

    def test_accept_mimetype(self, accept_mimetype):
        mimestrings = [[("Accept", "application/json")], [("Accept", "text/html")]]
        assert accept_mimetype in mimestrings

    def test_accept_any(self, accept_any):
        mimestrings = [[("Accept", "*")], [("Accept", "*/*")]]
        assert accept_any in mimestrings


@pytest.mark.usefixtures("client_class")
class TestClientClass:
    def test_client_attribute(self):
        assert hasattr(self, "client")
        assert self.client.get(url_for("ping")).json == {"ping": "pong"}
