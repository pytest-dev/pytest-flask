Getting started
===============


Step 1. Install
---------------

pytest-flask is available on `PyPi <https://pypi.python.org/pypi/pytest-flask>`_,
and can be easily installed via ``pip``::

    pip install pytest-flask


Step 2. Configure
-----------------

Define your application fixture in ``conftest.py``:

.. code:: python

    from myapp import create_app

    @pytest.fixture
    def app():
        app = create_app()
        return app


Step 3. Run your test suite
---------------------------

Use the ``py.test`` command to run your test suite::

    py.test

.. note:: Test discovery.

    py.test `discovers your tests <http://pytest.org/latest/goodpractises.html#python-test-discovery>`_
    and has a built-in integration with other testing tools (such as ``nose``,
    ``unittest`` and ``doctest``). More comprehensive examples and use cases
    can be found in the `official documentation <http://pytest.org/latest/usage.html>`_.
