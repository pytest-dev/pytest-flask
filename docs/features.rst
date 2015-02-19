.. _features:

Feature reference
=================

Fixtures
--------

``pytest-flask`` provides a list of useful fixtures to simplify application
testing. More information on fixtures and their usage is available in the
`py.test documentation <http://pytest.org/latest/fixture.html>`_.


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


Markers
-------

``pytest-flask`` registers the following markers. See the py.test
documentation_ on what marks are and for notes on using_ them.

.. _documentation: http://pytest.org/latest/mark.html
.. _using: http://pytest.org/latest/example/markers.html#marking-whole-classes-or-modules


``pytest.mark.app`` - pass options to your application config
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. py:function:: pytest.mark.app(**kwargs)

   The mark uses to pass options to your application config.

   :type kwargs: dict
   :param kwargs:
     The dictionary uses to extend application config.

   Example usage:

   .. code:: python

       @pytest.mark.app(debug=False)
       def test_app(app):
           assert not app.debug, 'Ensure the app not in debug mode'
