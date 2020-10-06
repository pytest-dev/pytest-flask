pytest-flask
============

|PyPI version| |conda-forge version| |Python versions| |ci| |Documentation status|

An extension of `pytest`_ test runner which
provides a set of useful tools to simplify testing and development
of the Flask extensions and applications.

To view a more detailed list of extension features and examples go to
the `PyPI`_ overview page or
`package documentation`_.

How to start?
-------------

Considering the minimal flask `application factory`_ bellow in ``myapp.py`` as an example:

.. code-block:: python

   from flask import Flask

   def create_app(config_filename):
      # create a minimal app
      app = Flask(__name__)
      app.config.from_pyfile(config_filename)

      # simple hello world view
      @app.route('/hello')
      def hello():
         return 'Hello, World!'

      return app

You first need to define your application fixture in ``conftest.py``:

.. code-block:: python

    from myapp import create_app

    @pytest.fixture
    def app():
        app = create_app()
        return app

Finally, install the extension with dependencies and run your test suite::

    $ pip install pytest-flask
    $ pytest

Contributing
------------

Don’t hesitate to create a `GitHub issue`_ for any bug or
suggestion.

.. |PyPI version| image:: https://img.shields.io/pypi/v/pytest-flask.svg
   :target: https://pypi.python.org/pypi/pytest-flask
   :alt: PyPi version

.. |conda-forge version| image:: https://img.shields.io/conda/vn/conda-forge/pytest-flask.svg
   :target: https://anaconda.org/conda-forge/pytest-flask
   :alt: conda-forge version

.. |ci| image:: https://github.com/pytest-dev/pytest-flask/workflows/build/badge.svg
   :target: https://github.com/pytest-dev/pytest-flask/actions
   :alt: CI status

.. |Python versions| image:: https://img.shields.io/pypi/pyversions/pytest-flask.svg
   :target: https://pypi.org/project/pytest-flask
   :alt: PyPi downloads

.. |Documentation status| image:: https://readthedocs.org/projects/pytest-flask/badge/?version=latest
   :target: https://pytest-flask.readthedocs.org/en/latest/
   :alt: Documentation status

.. _pytest: https://docs.pytest.org/en/stable/
.. _PyPI: https://pypi.python.org/pypi/pytest-flask
.. _Github issue: https://github.com/vitalk/pytest-flask/issues
.. _package documentation: http://pytest-flask.readthedocs.org/en/latest/
.. _application factory: https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/
