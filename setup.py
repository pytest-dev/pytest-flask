#!/usr/bin/env python
from pathlib import Path

from setuptools import setup

requirements = Path("requirements/main.txt").read_text(encoding="UTF-8").splitlines()
extras_require = {
    "docs": Path("requirements/docs.txt").read_text(encoding="UTF-8").splitlines(),
    "tests": Path("requirements/test.txt").read_text(encoding="UTF-8").splitlines(),
}

setup(
    # Dependencies are here for GitHub's dependency graph.
    use_scm_version={"write_to": "src/pytest_flask/_version.py"},
    install_requires=requirements,
    extras_require=extras_require,
)
