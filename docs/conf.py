# docs/conf.py
import os
import sys

# Para conseguir fazer autodoc de pyfwf
sys.path.insert(0, os.path.abspath(".."))

project = "python-pyfwf"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",  # se usar docstring Google/NumPy
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Sphinx 6+ usa root_doc; compatível com master_doc = "index"
root_doc = "index"

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
}
