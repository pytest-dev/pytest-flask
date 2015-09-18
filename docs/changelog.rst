.. _changelog:

Changelog
=========

Upcomming release
-----------------

- Add changelog to documentation.

0.10.0 (compared to 0.9.0)
--------------------------

- Add ``--start-live-server``/``--no-start-live-server`` options to prevent
  live server from starting automatically (#36), thanks to @EliRibble.

- Fix title formatting in documentation.

0.9.0 (compared to 0.8.1)
-------------------------

- Rename marker used to pass options to application, e.g. ``pytest.mark.app``
  is now ``pytest.mark.options`` (#35).

- Documentation badge points to the package documentation.

- Add Travis CI configuration to ensure the tests are passed in supported
  environments (#32).

0.8.1
-----

- Minor changes in documentation.

0.8.0
-----

- New ``request_ctx`` fixture which contains all request relevant
  information (#29).

0.7.5
-----

- Use pytest ``monkeypath`` fixture to teardown application config (#27).

0.7.4
-----

- Better test coverage, e.g. tests for available fixtures and markers.

0.7.3
-----

- Use retina-ready badges in documentation (#21).

0.7.2
-----

- Use pytest ``monkeypatch`` fixture to rewrite live server name.

0.7.1
-----

- Single-sourcing package version (#24), as per `"Python Packaging User Guide"
  <https://packaging.python.org/en/latest/single_source_version.html#single-sourcing-the-version>`_.

0.7.0
-----

- Add package documentation (#20).

0.6.3
-----

- Better documentation in README with reST formatting (#18), thanks to @greedo.

0.6.2
-----

- Release the random port before starting the application live server (#17),
  thanks to @davehunt.

0.6.1
-----

- Bind live server to a random port instead of 5000 or whatever is passed on
  the command line, so it's possible to execute tests in parallel via
  pytest-dev/pytest-xdist (#15). Thanks to @davehunt.

- Remove ``--liveserver-port`` option.

0.6.0
-----

- Fix typo in option help for ``--liveserver-port``, thanks to @svenstaro.

0.5.0
-----

- Add ``live_server`` fixture uses to run application in the background (#11),
  thanks to @svenstaro.

0.4.0
-----

- Add ``client_class`` fixture for class-based tests.

0.3.4
-----

- Include package requirements into distribution (#8).

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
