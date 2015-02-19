Welcome to pytest-flask's documentation!
========================================

A set of `py.test <http://pytest.org>`_ fixtures to test `Flask
<http://flask.pocoo.org>`_ extensions and applications.

.. toctree::
   :maxdepth: 2

   tutorial
   markers


Quickstart
==========

Install plugin via ``pip``::

    pip install pytest-flask

Define your application fixture in ``conftest.py``:

.. code:: python

    from myapp import create_app

    @pytest.fixture
    def app():
        app = create_app()
        return app

And run your test suite::

    py.test


Contributing
============

Don't hesitate to create a `GitHub issue
<https://github.com/vitalk/pytest-flask/issues>`_ for any **bug** or
**suggestion**.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
