import nox

@nox.session(python=False)
def build(session):
    session.install("poetry")
    session.run("poetry", "shell")
    session.run("poetry", "install")

@nox.session(python=False)
def tests(session):
    session.run("pytest", "tests/")

@nox.session(python=False)
def lint(session):
    session.run("flake8", "--max-line-length", "120", "main.py")

@nox.session(python=False)
def type(session):
    session.run("mypy", "--ignore-missing-imports", "main.py")