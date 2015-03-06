#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest


class TestAppMarker:

    @pytest.mark.app(debug=False)
    def test_not_debug_app(self, app):
        assert not app.debug, 'Ensure the app not in debug mode'

    @pytest.mark.app(foo=42)
    def test_update_application_config(self, config):
        assert config['FOO'] == 42
