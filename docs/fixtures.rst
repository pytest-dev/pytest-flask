Fixtures
========

Plugin provides some useful fixtures to simplify application testing and
development. More information on fixtures is available in the `py.test
documentation <http://pytest.org/latest/fixture.html>`_.


``client`` - application test client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An instance of ``app.test_client``. Typically refers to
`flask.Flask.test_client <http://flask.pocoo.org/docs/latest/api/#flask.Flask.test_client>`_.

.. note::

    During tests execution the application has pushed context, e.g.
    ``url_for``, ``session`` and other context bound objects are available
    without context managers.

Example:
""""""""

.. code:: python

    def test_myview(client):
        assert client.get(url_for('myview')).status_code == 200


``client_class`` - application test client for class-based tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example:
""""""""

.. code:: python

    @pytest.mark.usefixtures('client_class')
    class TestSuite:

        def test_myview(self):
            assert self.client.get(url_for('myview')).status_code == 200


``config`` - application config
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An instance of ``app.config``. Typically refers to `flask.Flask.Config <http://flask.pocoo.org/docs/latest/api/#flask.Flask.config>`_.


``live_server`` - application live server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run application in a separate process (useful for tests with Selenium_ and
other headless browsers).

.. note::

    The server's URL can be retrieved using the ``url_for`` function.

.. code:: python

    from flask import url_for

    @pytest.mark.usefixtures('live_server')
    class TestLiveServer:

        def test_server_is_up_and_running(self):
            res = urllib2.urlopen(url_for('index', _external=True))
            assert b'OK' in res.read()
            assert res.code == 200

.. _Selenium: http://www.seleniumhq.org
