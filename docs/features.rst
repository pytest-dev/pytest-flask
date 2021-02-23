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

    User-defined ``json`` attribute/method in application response class will
    not be overwritten. So you can define your own response deserialization method:

    .. code:: python

        from flask import Response
        from myapp import create_app

        class MyResponse(Response):
            '''Implements custom deserialization method for response objects.'''
            @property
            def json(self):
                return 42

        @pytest.fixture(scope="session")
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

    pytest -n <number of processes>

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

    During test execution a request context will be automatically pushed
    for you, so context-bound methods can be conveniently called (e.g.
    ``url_for``, ``session``.

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

By default the server will start automatically whenever you reference
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


``--live-server-wait`` - the live server wait timeout (5 seconds)
`````````````````````````````````````````````````````````````````
The timeout after which test case is aborted if live server is not started.


``--live-server-port`` - use a fixed port
`````````````````````````````````````````
By default the server uses a random port. In some cases it is desirable to run
the server with a fixed port. You can use ``--live-server-port`` (for example,
in your project's ``pytest.ini`` file)::

    [pytest]
    addopts = --live-server-port=5000


``request_ctx`` - request context (Deprecated)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**This fixture is deprecated and will be removed in the future.**

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


``live_server_scope`` - set the scope of the live server
``````````````````````````````````````````````````````````````````

By default, the server will be scoped to ``session`` for performance reasons, however
if your server has global state and you want better test isolation, you can use the
``live_server_scope`` ini option to change the fixture scope:

.. code-block:: ini

    [pytest]
    live_server_scope = function


HTTP Request
~~~~~~~~~~~~~~~~~~~

Common request methods are available through the internals of the `Flask API`_.
Specifically, the API creates the default `flask.Flask.test_client`_ instance,
which works like a regular `Werkzeug test client`_.

Examples:

.. code:: python

    def test_post_request(client, live_server):
        @live_server.app.route('/load-data')
        def get_endpoint():
            return url_for('name.load', _external=True)

        live_server.start()

        res = client.post(
            get_endpoint(),
            headers={'Content-Type': 'application/json'},
            data={}
        )

        assert res.status_code == 200

.. code:: python

    def test_get_request(client, live_server):
        @live_server.app.route('/load-data')
        def get_endpoint():
            return url_for('name.load', _external=True)

        live_server.start()

        res = client.get(get_endpoint())

        assert res.status_code == 200

.. note::

    The notation ``name.load_data``, corresponds to a ``endpoint='load'``
    attribute, within a route decorator. The following is a route decorator
    using the `blueprint`_ implementation:

        .. code:: python

            from flask import Blueprint, request

            # local variables
            blueprint = Blueprint(
                'name',
                __name__,
                template_folder='interface/templates',
                static_folder='interface/static'
            )

            @blueprint.route('/load-data', methods=['POST'], endpoint='load')
            def load_data():
                if request.method == 'POST':
                    if request.get_json():
                        pass

Alternatively, the route function can be referenced directly from the
``live_server`` implementation, rather than implementing an ``endpoint``:

    .. code:: python

        def test_load_data(live_server, client):
            @live_server.app.route('/load-data', methods=['POST'])
            def load_data():
                pass

            live_server.start()

            res = client.post(url_for('load_data'), data={})
            assert res.status_code == 200

.. note::

    Remember to explicitly define which ``methods`` are supported when
    registering the above route function.


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
           assert not app.debug, 'Ensure the app is not in debug mode'


.. _pytest-xdist: https://pypi.python.org/pypi/pytest-xdist
.. _pytest documentation: https://pytest.org/en/latest/fixture.html
.. _flask.Flask.test_client: https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.test_client
.. _flask.Config: https://flask.palletsprojects.com/en/1.1.x/api/#flask.Config
.. _Selenium: https://selenium-python.readthedocs.io/
.. _what markers are: https://pytest.org/en/latest/mark.html
.. _using them: https://pytest.org/en/latest/example/markers.html#marking-whole-classes-or-modules
.. _Flask API: https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.test_client
.. _Werkzeug test client: https://werkzeug.palletsprojects.com/en/1.0.x/test/#werkzeug.test.Client
.. _blueprint: https://flask.palletsprojects.com/en/1.1.x/blueprints/
