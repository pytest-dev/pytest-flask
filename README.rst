|PyPI version|

pytest-flask
============

A set of pytest fixtures to test Flask applications.


What is it?
-----------

An extension of `pytest <http://pytest.org/>`__ test runner which
provides a set of useful tools to simplify testing and development
of the Flask extensions and applications.

To view a more detailed list of extension features and examples go to
the PyPI overview `page <https://pypi.python.org/pypi/pytest-flask>`__.

How to start?
-------------

Define your application fixture in `conftest.py`::

    from myapp import create_app

    @pytest.fixture
    def app():
        app = create_app()
        return app

Install the extension with dependencies and go::

    $ pip install pytest-flask
    $ py.test

Contributing
------------

Don't hesitate to create a `GitHub issue <https://github.com/vitalk/pytest-flask/issues>`__ for any bug or
suggestion.

.. |PyPI version| image:: https://badge.fury.io/py/pytest-flask.png
   :target: http://badge.fury.io/py/pytest-flask
