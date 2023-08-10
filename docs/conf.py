# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sphinx_rtd_theme
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'RCTab'
copyright = '2023, The Alan Turing Institute'
author = 'The Alan Turing Institute'

sys.path.append(os.path.abspath('../rctab-infrastructure/src'))
sys.path.append(os.path.abspath('../rctab-cli/rctab_cli'))
sys.path.append(os.path.abspath('../rctab-functions/controller_function/controller'))
sys.path.append(os.path.abspath('../rctab-functions/status_function/status'))

os.environ["SPHYNX_AUTODOC_MODE"] = "true"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser", "sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx.ext.autosummary"]

autosummary_generate = True
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['_static']

html_logo = 'RCTab-hex.png'
html_theme_options = {
    'logo_only': True,
    'display_version': True,
}

def setup (app):
    app.add_css_file('css/custom.css')
