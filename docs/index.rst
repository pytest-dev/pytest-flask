Welcome to pytest-flask’s documentation!
========================================

Pytest-flask is a plugin for `pytest <http://pytest.org>`_ that provides
a set of useful tools to test `Flask <http://flask.pocoo.org>`_ applications
and extensions.


Quickstart
----------

Install plugin via ``pip``::

    pip install pytest-flask

Define your application fixture in ``conftest.py``:

.. code:: python

    from myapp import create_app

    @pytest.fixture
    def app():
        app = create_app()
        return app

Now you can use the ``app`` fixture in your test suite. You can run your tests
with::

    pytest


User’s Guide
------------

This part of the documentation will show you how to get started in using
pytest-flask with your application.

.. toctree::
   :maxdepth: 4

   tutorial
   features
   contributing
   changelog
