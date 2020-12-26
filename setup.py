#!/usr/bin/env python
import os

from setuptools import find_packages
from setuptools import setup


def read(*parts):
    """Reads the content of the file located at path created from *parts*."""
    try:
        return open(os.path.join(*parts), "r", encoding="utf-8").read()
    except OSError:
        return ""


tests_require = []
requirements = read("requirements", "main.txt").splitlines()
extras_require = {
    "docs": read("requirements", "docs.txt").splitlines(),
    "tests": tests_require,
}

setup(
    # Dependencies are here for GitHub's dependency graph.
    use_scm_version={"write_to": "pytest_flask/_version.py"},
    install_requires=requirements,
    tests_require=tests_require,
    extras_require=extras_require,
)
