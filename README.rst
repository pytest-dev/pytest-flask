pytest-flask
============

|PyPI version| |PyPI downloads| |Documentation status|

An extension of `pytest <http://pytest.org/>`__ test runner which
provides a set of useful tools to simplify testing and development
of the Flask extensions and applications.

To view a more detailed list of extension features and examples go to
the `PyPI <https://pypi.python.org/pypi/pytest-flask>`__ overview page or
`package documentation <http://pytest-flask.readthedocs.org/en/latest/>`_.

How to start?
-------------

Define your application fixture in ``conftest.py``::

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

.. |PyPI version| image:: https://img.shields.io/pypi/v/pytest-flask.svg
   :target: https://pypi.python.org/pypi/pytest-flask
   :alt: PyPi version

.. |PyPI downloads| image:: https://img.shields.io/pypi/dm/pytest-flask.svg
   :target: https://pypi.python.org/pypi/pytest-flask
   :alt: PyPi downloads

.. |Documentation status| image:: https://readthedocs.org/projects/pytest-flask/badge/?version=latest
   :target: https://readthedocs.org/projects/pytest-flask/?badge=latest
   :alt: Documentation status
