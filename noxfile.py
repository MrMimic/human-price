import os
import sys

import nox


@nox.session(python=False)
def build(session):
    # Install dependencies
    session.install("--upgrade", "pip")
    session.install("poetry")
    session.run("poetry", "shell")
    session.run("poetry", "install")
    # Update pythonpath
    src_folder = os.path.join("src", "python")
    sys.path.append(src_folder)
    os.environ["PYTHONPATH"] = "/src/python"


@nox.session(python=False)
def tests(session):
    session.run("pytest", "tests/")


@nox.session(python=False)
def lint(session):
    session.run("flake8", "--max-line-length", "120", "main.py", "src/python/")


@nox.session(python=False)
def type(session):
    session.run("mypy", "--ignore-missing-imports", "main.py", "src/python/")
