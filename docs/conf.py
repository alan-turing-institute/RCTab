"""Configuration file for the Sphinx documentation builder."""
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sphinx_rtd_theme
import sys

# -- Project information

project = "RCTab"
author = "The Alan Turing Institute"
copyright = f"2023, {author}"

# -- General configuration

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    #    "subprojecttoctree",
]

# -- Intersphinx configuration

# intersphinx_mapping = {
#    'python': ('https://docs.python.org/3/', None),
#    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
#    'mysub': ('https://rctab.readthedocs.io/projects/rctab-cli/en/latest/', None),
# }
# intersphinx_disabled_domains = ['std']

# We recommend adding the following config value.
# Sphinx defaults to automatically resolve *unresolved* labels using all your Intersphinx mappings.
# This behavior has unintended side-effects, namely that documentations local references can
# suddenly resolve to an external location.
# See also:
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#confval-intersphinx_disabled_reftypes
# intersphinx_disabled_reftypes = ["*"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ["_static"]

html_logo = "RCTab-hex.png"
html_theme_options = {
    "logo_only": True,
    "display_version": True,
}


def setup(app):
    app.add_css_file("css/custom.css")


# -- Options for Subprojecttoctree

# is_subproject = False
# readthedocs_url = "https://rctab.readthedocs.io"

autosummary_generate = True
