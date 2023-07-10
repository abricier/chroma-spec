"""Nox sessions."""

import os
import shutil
import sys
from pathlib import Path
from textwrap import dedent

import nox

try:
    from nox_poetry import Session, session
except ImportError:
    message = f"""\
    Nox failed to import the 'nox-poetry' package.
    Please install it using the following command:
    {sys.executable} -m pip install nox-poetry"""
    raise SystemExit(dedent(message)) from None


package = "chroma_spec"
python_versions = ["3.10"]
nox.options.sessions = "lint", "tests", "coverage"
nox.needs_version = ">= 2023.4.22"
locations = "chroma_spec", "tests", "docs", "noxfile.py", "docs/conf.py"


@session(python=python_versions)
def black(session):
    """Code formatting with Black."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@session(python=python_versions)
def tests(session):
    """Testing with pytest."""
    session.install(".")
    session.install("coverage[toml]", "pytest", "jsonschema")
    try:
        session.run("coverage", "run", "--parallel", "-m", "pytest", *session.posargs)
    finally:
        if session.interactive:
            session.notify("coverage", posargs=[])


@session(python=python_versions)
def coverage(session) -> None:
    """Produce the coverage report."""
    args = session.posargs or ["report"]
    session.install("coverage[toml]")
    if not session.posargs and any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")
    session.run("coverage", *args)
    if session.interactive:
        session.notify("coverage-html", posargs=[])


@session(name="coverage-html", python=python_versions)
def coverage_html(session) -> None:
    """Produce the coverage html report."""
    html_dir = Path("htmlcov")
    if html_dir.exists():
        shutil.rmtree(html_dir)
    args = session.posargs or ["html"]
    session.install("coverage[toml]")
    session.run("coverage", *args)


@session(python=python_versions)
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    if session.posargs:
        args = [package, *session.posargs]
    else:
        args = [f"--modname={package}", "--command=all"]
        if "FORCE_COLOR" in os.environ:
            args.append("--colored=1")

    session.install(".")
    session.install("xdoctest[colors]")
    session.run("python", "-m", "xdoctest", *args)


@session(python=python_versions)
def lint(session):
    """Linting with Flake8."""
    args = session.posargs or locations
    session.install(
        "darglint",
        "flake8",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-isort",
        "flake8-rst-docstrings",
        "pep8-naming",
    )
    session.run("flake8", *args)


@session(python=python_versions)
def docs(session: Session) -> None:
    """Build the documentation."""
    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    args = session.posargs or ["docs", "docs/_build"]
    session.install(".")
    session.install("sphinx", "sphinx-click", "furo", "myst-parser")
    session.run("sphinx-build", *args)


@session(name="docs-serve", python=python_versions)
def docs_serve(session: Session) -> None:
    """Build and serve the documentation with live reloading on file changes."""
    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    args = session.posargs or ["--open-browser", "docs", "docs/_build"]
    session.install(".")
    session.install("sphinx", "sphinx-autobuild", "sphinx-click", "furo", "myst-parser")
    session.run("sphinx-autobuild", *args)
