Getting started
===============

Pytest is capable to pick up and run existing tests without any or little
configuration. This section describes how to get started quickly.

Step 1. Install
---------------

``pytest-flask`` is available on `PyPi`_, and can be easily installed via
``pip``::

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

    Pytest `discovers your tests`_ and has a built-in integration with other
    testing tools (such as ``nose``, ``unittest`` and ``doctest``). More
    comprehensive examples and use cases can be found in the `official
    documentation`_.


What’s next?
------------

The :ref:`features` section gives a more detailed view of available features, as
well as test fixtures and markers.

Consult the `pytest documentation <http://pytest.org/latest>`_ for more
information about pytest itself.

If you want to contribute to the project, see the :ref:`contributing` section.


.. _PyPi: https://pypi.python.org/pypi/pytest-flask
.. _discovers your tests: http://docs.pytest.org/en/latest/goodpractices.html#test-discovery
.. _official documentation: http://pytest.org/latest/usage.html
