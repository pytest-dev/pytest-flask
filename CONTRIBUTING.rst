How to contribute
=================

All contributions are greatly appreciated!

How to report issues
~~~~~~~~~~~~~~~~~~~~

Facilitating the work of potential contributors is recommended since it
increases the likelihood of your issue being solved quickly. The few extra
steps listed below will help clarify problems you might be facing:

-   Include a `minimal reproducible example`_ when possible.
-   Describe the expected behaviour and what actually happened including a full
    trace-back in case of exceptions.
-   Make sure to list details about your environment, such as your platform,
    versions of pytest, pytest-flask and python release.

Also, it's important to check the current open issues for similar reports
in order to avoid duplicates.

.. _minimal reproducible example: https://stackoverflow.com/help/minimal-reproducible-example

Setting up your development environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   Fork pytest-flask to your GitHub account by clicking the `Fork`_ button.
-   `Clone`_ the main repository (not your fork) to your local machine.

    .. code-block:: text

        $ git clone https://github.com/pytest-dev/pytest-flask
        $ cd pytest-flask

-   Add your fork as a remote to push your contributions.Replace
    ``{username}`` with your username.

    .. code-block:: text

        git remote add fork https://github.com/{username}/pytest-flask

-   Using `Tox`_, create a virtual environment and install pytest-flask in editable mode with development dependencies.

    .. code-block:: text

        $ tox -e dev
        $ source venv/bin/activate

-   Install pre-commit hooks

    .. code-block:: text

        $ pre-commit install

.. _Fork: https://github.com/pytest-dev/pytest-flask/fork
.. _Clone: https://help.github.com/en/articles/fork-a-repo#step-2-create-a-local-clone-of-your-fork
.. _Tox: https://tox.readthedocs.io/en/latest/

Start Coding
~~~~~~~~~~~~

-   Create a new branch to identify what feature you are working on.

    .. code-block:: text

        $ git fetch origin
        $ git checkout -b your-branch-name origin/master

-   Make your changes
-   Include tests that cover any code changes you make and run them
    as described below.
-   Push your changes to your fork.
    `create a pull request`_ describing your changes.

    .. code-block:: text

        $ git push --set-upstream fork your-branch-name

.. _create a pull request: https://help.github.com/en/articles/creating-a-pull-request

How to run tests
~~~~~~~~~~~~~~~~

You can run the test suite for the current environment with

    .. code-block:: text

        $ pytest

To run the full test suite for all supported python versions

    .. code-block:: text

        $ tox

Obs. CI will run tox when you submit your pull request, so this is optional.

Checking Test Coverage
~~~~~~~~~~~~~~~~~~~~~~~

To get a complete report of code sections not being touched by the
test suite run ``pytest`` using ``coverage``.

.. code-block:: text
    $ coverage run --concurrency=multiprocessing -m pytest
    $ coverage combine
    $ coverage html

Open ``htmlcov/index.html`` in your browser.

More about converage `here <https://coverage.readthedocs.io>`__.
