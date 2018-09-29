.. _features:

Feature reference
=================

Extension provides some sugar for your tests, such as:

* Access to context bound objects (``url_for``, ``request``, ``session``)
  without context managers:

  .. code:: python

    def test_app(client):
        assert client.get(url_for('myview')).status_code == 200

* Easy access to ``JSON`` data in response:

  .. code:: python

    @api.route('/ping')
    def ping():
        return jsonify(ping='pong')

    def test_api_ping(client):
        res = client.get(url_for('api.ping'))
        assert res.json == {'ping': 'pong'}

  .. note::

    User-defined ``json`` attribute/method in application response class does
    not overrides. So you can define your own response deserialization method:

    .. code:: python

        from flask import Response
        from myapp import create_app

        class MyResponse(Response):
            '''Implements custom deserialization method for response objects.'''
            @property
            def json(self):
                '''What is the meaning of life, the universe and everything?'''
                return 42

        @pytest.fixture
        def app():
            app = create_app()
            app.response_class = MyResponse
            return app

        def test_my_json_response(client):
            res = client.get(url_for('api.ping'))
            assert res.json == 42

* Running tests in parallel with `pytest-xdist`_. This can lead to
  significant speed improvements on multi core/multi CPU machines.

  This requires the ``pytest-xdist`` plugin to be available, it can usually be
  installed with::

    pip install pytest-xdist

  You can then run the tests by running::

    py.test -n <number of processes>

**Not enough pros?** See the full list of available fixtures and markers
below.


Fixtures
--------

``pytest-flask`` provides a list of useful fixtures to simplify application
testing. More information on fixtures and their usage is available in the
`pytest documentation`_.


``client`` - application test client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An instance of ``app.test_client``. Typically refers to
`flask.Flask.test_client`_.

.. hint::

    During tests execution the request context has been pushed, e.g.
    ``url_for``, ``session`` and other context bound objects are available
    without context managers.

Example:

.. code:: python

    def test_myview(client):
        assert client.get(url_for('myview')).status_code == 200


``client_class`` - application test client for class-based tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example:

.. code:: python

    @pytest.mark.usefixtures('client_class')
    class TestSuite:

        def test_myview(self):
            assert self.client.get(url_for('myview')).status_code == 200


``config`` - application config
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An instance of ``app.config``. Typically refers to `flask.Config`_.


``live_server`` - application live server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run application in a separate process (useful for tests with Selenium_ and
other headless browsers).

.. hint::

    The server’s URL can be retrieved using the ``url_for`` function.

.. code:: python

    from flask import url_for

    @pytest.mark.usefixtures('live_server')
    class TestLiveServer:

        def test_server_is_up_and_running(self):
            res = urllib2.urlopen(url_for('index', _external=True))
            assert b'OK' in res.read()
            assert res.code == 200


``--start-live-server`` - start live server automatically (default)
```````````````````````````````````````````````````````````````````


``--no-start-live-server`` - don’t start live server automatically
``````````````````````````````````````````````````````````````````

By default the server is starting automatically whenever you reference
``live_server`` fixture in your tests. But starting live server imposes some
high costs on tests that need it when they may not be ready yet. To prevent
that behaviour pass ``--no-start-live-server`` into your default options (for
example, in your project’s ``pytest.ini`` file)::

    [pytest]
    addopts = --no-start-live-server

.. note::

    You **should manually start** live server after you finish your application
    configuration and define all required routes:

    .. code:: python

        def test_add_endpoint_to_live_server(live_server):
            @live_server.app.route('/test-endpoint')
            def test_endpoint():
                return 'got it', 200

            live_server.start()

            res = urlopen(url_for('test_endpoint', _external=True))
            assert res.code == 200
            assert b'got it' in res.read()


``--live-server-port`` - use a fixed port
`````````````````````````````````````````

By default the server uses a random port. In some cases it is desirable to run
the server with a fixed port. You can use ``--live-server-port`` (for example,
in your project's ``pytest.ini`` file)::

    [pytest]
    addopts = --live-server-port=5000


``request_ctx`` - request context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The request context which contains all request relevant information.

.. hint::

    The request context has been pushed implicitly any time the ``app``
    fixture is applied and is kept around during test execution, so it’s easy
    to introspect the data:

    .. code:: python

        from flask import request, url_for

        def test_request_headers(client):
            res = client.get(url_for('ping'), headers=[('X-Something', '42')])
            assert request.headers['X-Something'] == '42'


Content negotiation
~~~~~~~~~~~~~~~~~~~

An important part of any :abbr:`REST (REpresentational State Transfer)`
service is content negotiation. It allows you to implement behaviour such as
selecting a different serialization schemes for different media types.

    HTTP has provisions for several mechanisms for "content negotiation" - the
    process of selecting the best representation for a given response
    when there are multiple representations available.

    -- :rfc:`2616#section-12`. Fielding, et al.

The most common way to select one of the multiple possible representation is
via ``Accept`` request header. The following series of ``accept_*`` fixtures
provides an easy way to test content negotiation in your application:

.. code:: python

    def test_api_endpoint(accept_json, client):
        res = client.get(url_for('api.endpoint'), headers=accept_json)
        assert res.mimetype == 'application/json'


``accept_any`` - :mimetype:`*/*` accept header
``````````````````````````````````````````````

:mimetype:`*/*` accept header suitable to use as parameter in ``client``.


``accept_json`` - :mimetype:`application/json` accept header
````````````````````````````````````````````````````````````

:mimetype:`application/json` accept header suitable to use as parameter in
``client``.


``accept_jsonp`` - :mimetype:`application/json-p` accept header
```````````````````````````````````````````````````````````````

:mimetype:`application/json-p` accept header suitable to use as parameter in
``client``.


Markers
-------

``pytest-flask`` registers the following markers. See the pytest documentation
on `what markers are`_ and for notes on `using them`_.


``pytest.mark.options`` - pass options to your application config
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. py:function:: pytest.mark.options(**kwargs)

   The mark used to pass options to your application config.

   :type kwargs: dict
   :param kwargs:
     The dictionary used to extend application config.

   Example usage:

   .. code:: python

       @pytest.mark.options(debug=False)
       def test_app(app):
           assert not app.debug, 'Ensure the app not in debug mode'


.. _pytest-xdist: https://pypi.python.org/pypi/pytest-xdist
.. _pytest documentation: http://pytest.org/latest/fixture.html
.. _flask.Flask.test_client: http://flask.pocoo.org/docs/latest/api/#flask.Flask.test_client
.. _flask.Config: http://flask.pocoo.org/docs/latest/api/#flask.Config
.. _Selenium: http://www.seleniumhq.org
.. _what markers are: http://pytest.org/latest/mark.html
.. _using them: http://pytest.org/latest/example/markers.html#marking-whole-classes-or-modules
