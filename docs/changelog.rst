.. _changelog:

Changelog
=========

0.15.0 (2019-05-13)
-------------------

- Properly register the ``options`` marker (`#97`_).

.. _#97: https://github.com/pytest-dev/pytest-flask/pull/97

0.14.0 (2018-10-15)
-------------------

- New ``--live-server-host`` command-line option to set the host name used by
  the ``live_server`` fixture.

  Thanks `@o1da`_ for the PR (`#90`_).

.. _@o1da: https://github.com/o1da
.. _#90: https://github.com/pytest-dev/pytest-flask/pull/90

0.13.0 (2018-09-29)
-------------------

- ``JSONReponse`` now supports comparison directly with status codes:

  .. code-block:: python

      assert client.get('invalid-route', headers=[('Accept', 'application/json')]) == 404

  Thanks `@dusktreader`_ for the PR (`#86`_).

.. _@dusktreader: https://github.com/dusktreader
.. _#86: https://github.com/pytest-dev/pytest-flask/pull/86

0.12.0 (2018-09-06)
-------------------

- ``pytest-flask`` now requires ``pytest>=3.6`` (`#84`_).

- Add new ``--live-server-port`` option to select the port the live server will use (`#82`_).
  Thanks `@RazerM`_ for the PR.

- Now ``live_server`` will try to stop the server cleanly by emitting a ``SIGINT`` signal and
  waiting 5 seconds for the server to shutdown. If the server is still running after 5 seconds,
  it will be forcefully terminated. This behavior can be changed by passing
  ``--no-live-server-clean-stop`` in the command-line (`#49`_).
  Thanks `@jadkik`_ for the PR.

- Internal fixes silence pytest warnings, more visible now with ``pytest-3.8.0`` (`#84`_).

.. _@jadkik: https://github.com/jadkik
.. _@RazerM: https://github.com/RazerM
.. _#49: https://github.com/pytest-dev/pytest-flask/issues/49
.. _#82: https://github.com/pytest-dev/pytest-flask/pull/82
.. _#84: https://github.com/pytest-dev/pytest-flask/pull/84


0.11.0 (compared to 0.10.0)
---------------------------

- Implement deployment using Travis, following in line with many other pytest plugins.

- Allow live server to handle concurrent requests (`#56`_), thanks to
  `@mattwbarry`_ for the PR.

- Fix broken link to pytest documentation (`#50`_), thanks to
  `@jineshpaloor`_ for the PR.

- Tox support (`#48`_), thanks to `@steenzout`_ for the PR.

- Add ``LICENSE`` into distribution (`#43`_), thanks to `@danstender`_.

- Minor typography improvements in documentation.

- Add changelog to documentation.


.. _#43: https://github.com/vitalk/pytest-flask/issues/43
.. _#48: https://github.com/pytest-dev/pytest-flask/pull/48
.. _#50: https://github.com/pytest-dev/pytest-flask/pull/50
.. _#56: https://github.com/pytest-dev/pytest-flask/pull/56
.. _@danstender: https://github.com/danstender
.. _@jineshpaloor: https://github.com/jineshpaloor
.. _@mattwbarry: https://github.com/mattwbarry
.. _@steenzout: https://github.com/steenzout


0.10.0 (compared to 0.9.0)
--------------------------

- Add ``--start-live-server``/``--no-start-live-server`` options to prevent
  live server from starting automatically (`#36`_), thanks to `@EliRibble`_.

- Fix title formatting in documentation.


.. _#36: https://github.com/vitalk/pytest-flask/issues/36
.. _@EliRibble: https://github.com/EliRibble


0.9.0 (compared to 0.8.1)
-------------------------

- Rename marker used to pass options to application, e.g. ``pytest.mark.app``
  is now ``pytest.mark.options`` (`#35`_).

- Documentation badge points to the package documentation.

- Add Travis CI configuration to ensure the tests are passed in supported
  environments (`#32`_).


.. _#32: https://github.com/vitalk/pytest-flask/issues/32
.. _#35: https://github.com/vitalk/pytest-flask/issues/35

0.8.1
-----

- Minor changes in documentation.

0.8.0
-----

- New ``request_ctx`` fixture which contains all request relevant
  information (`#29`_).

.. _#29: https://github.com/vitalk/pytest-flask/issues/29

0.7.5
-----

- Use pytest ``monkeypath`` fixture to teardown application config (`#27`_).

.. _#27: https://github.com/vitalk/pytest-flask/issues/27

0.7.4
-----

- Better test coverage, e.g. tests for available fixtures and markers.

0.7.3
-----

- Use retina-ready badges in documentation (`#21`_).

.. _#21: https://github.com/vitalk/pytest-flask/issues/21

0.7.2
-----

- Use pytest ``monkeypatch`` fixture to rewrite live server name.

0.7.1
-----

- Single-sourcing package version (`#24`_), as per `"Python Packaging User Guide"
  <https://packaging.python.org/en/latest/single_source_version.html#single-sourcing-the-version>`_.

.. _#24: https://github.com/vitalk/pytest-flask/issues/24

0.7.0
-----

- Add package documentation (`#20`_).

.. _#20: https://github.com/vitalk/pytest-flask/issues/20

0.6.3
-----

- Better documentation in README with reST formatting (`#18`_), thanks
  to `@greedo`_.


.. _#18: https://github.com/vitalk/pytest-flask/issues/18
.. _@greedo: https://github.com/greedo

0.6.2
-----

- Release the random port before starting the application live server (`#17`_),
  thanks to `@davehunt`_.


.. _#17: https://github.com/vitalk/pytest-flask/issues/17
.. _@davehunt: https://github.com/davehunt

0.6.1
-----

- Bind live server to a random port instead of 5000 or whatever is passed on
  the command line, so it’s possible to execute tests in parallel via
  pytest-dev/pytest-xdist (`#15`_). Thanks to `@davehunt`_.

- Remove ``--liveserver-port`` option.


.. _#15: https://github.com/vitalk/pytest-flask/issues/15
.. _@davehunt: https://github.com/davehunt

0.6.0
-----

- Fix typo in option help for ``--liveserver-port``, thanks to `@svenstaro`_.

.. _@svenstaro: https://github.com/svenstaro

0.5.0
-----

- Add ``live_server`` fixture uses to run application in the background (`#11`_),
  thanks to `@svenstaro`_.


.. _#11: https://github.com/vitalk/pytest-flask/issues/11
.. _@svenstaro: https://github.com/svenstaro

0.4.0
-----

- Add ``client_class`` fixture for class-based tests.

0.3.4
-----

- Include package requirements into distribution (`#8`_).

.. _#8: https://github.com/vitalk/pytest-flask/issues/8

0.3.3
-----

- Explicitly pin package dependencies and their versions.

0.3.2
-----

- Use ``codecs`` module to open files to prevent possible errors on open
  files which contains non-ascii characters.

0.3.1
-----

First release on PyPI.
