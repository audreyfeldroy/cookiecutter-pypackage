from {{cookiecutter.package_name}} import _version

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = '{{cookiecutter.project_name}}'

copyright = '2021, Marcus Michael Noack'
author = '{{cookiecutter.full_name}}'
version = _version.get_versions()['version']


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'myst_nb',
    'sphinx_panels',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon'
]

# MyST extensions
myst_enable_extensions = ['colon_fence']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

html_style = 'custom.css'

# html_theme = 'theme' # use the theme in subdir 'theme'
# html_theme_path = ['../'] # make sphinx search for themes in current dir

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_theme_display_version = True

html_theme_options = dict(
    logo_only=True,
    display_version=True,
    collapse_navigation=False,
    titles_only=False
)

# Configure execution (and output generation) of myst-nb files
jupyter_execute_notebooks = "off"
