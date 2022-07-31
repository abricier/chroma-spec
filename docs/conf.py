"""Sphinx configuration."""
from datetime import datetime

project = "chroma-spec"
author = "abr"
copyright = f"{datetime.now().year}, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
html_theme = "furo"
