=======================
Releasing pytest-flask
=======================

This document describes the steps to make a new ``pytest-flask`` release.

Version
-------

``master`` should always be green and a potential release candidate. ``pytest-flask`` follows
semantic versioning, so given that the current version is ``X.Y.Z``, to find the next version number
one needs to look at the ``docs/changelog.rst`` file.

Steps
-----

#. Create a new branch named ``release-X.Y.Z`` from the latest ``master``.

#. After making the necessary changes, commit and push the branch for review.

#. Once PR is **green** and **approved**, create and push a tag::

    $ export VERSION=X.Y.Z
    $ git tag $VERSION release-$VERSION
    $ git push git@github.com:pytest-dev/pytest-flask.git $VERSION

    That will build the package and publish it on ``PyPI`` automatically.

#. Merge ``release-X.Y.Z`` branch into master.
