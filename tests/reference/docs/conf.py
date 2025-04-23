# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
import urllib3
import shutil
import numpy as np
sys.path.insert(0, os.path.abspath('..'))

import imkar  # noqa

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'matplotlib.sphinxext.plot_directive',
    'sphinx.ext.mathjax',
    'sphinx.ext.intersphinx',
    'autodocsumm',
    'sphinx_design',
    'sphinx_favicon',
    'sphinx_reredirects',
    'sphinx_mdinclude',
]

# show tocs for classes and functions of modules using the autodocsumm
# package
autodoc_default_options = {'autosummary': True}

# show the code of plots that follows the command .. plot:: based on the
# package matplotlib.sphinxext.plot_directive
plot_include_source = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'imkar'
copyright = "2025, The pyfar developers"
author = "The pyfar developers"

# The version info for the project you're documenting, acts as replacement
# for |version| and |release|, also used in various other places throughout
# the built documents.
#
# The short X.Y version.
version = imkar.__version__
# The full version, including alpha/beta/rc tags.
release = imkar.__version__

# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use (Not defining
# uses the default style of the html_theme).
# pygments_style = 'sphinx'

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# default language for highlighting in source code
highlight_language = "python3"

# intersphinx mapping
intersphinx_mapping = {
    'numpy': ('https://numpy.org/doc/stable/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
    'pyfar': ('https://pyfar.readthedocs.io/en/stable/', None),
    }

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_css_files = ['css/custom.css']
html_logo = 'resources/logos/pyfar_logos_fixed_size_imkar.png'
html_title = "imkar"
html_favicon = '_static/favicon.ico'

# -- HTML theme options
# https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/layout.html
html_sidebars = {
  "imkar": []
}

html_theme_options = {
    "navbar_start": ["navbar-logo"],
    "navbar_end": ["navbar-icon-links", "theme-switcher"],
    "navbar_align": "content",
    "header_links_before_dropdown": 99,  # will be automatically set later based on headers.rst
    "header_dropdown_text": "Packages",  # Change dropdown name from "More" to "Packages"
    "icon_links": [
        {
          "name": "GitHub",
          "url": "https://github.com/pyfar",
          "icon": "fa-brands fa-square-github",
          "type": "fontawesome",
        },
    ],
    # Configure secondary (right) side bar
    "show_toc_level": 3,  # Show all subsections of notebooks
    "secondary_sidebar_items": ["page-toc"],  # Omit 'show source' link that that shows notebook in json format
    "navigation_with_keys": True,
    # Configure navigation depth for section navigation
    "navigation_depth": 1,
}

html_context = {
   "default_mode": "light"
}

# redirect index to pyfar.html
redirects = {
     "index": "imkar.html"
}

# -- download navbar and style files from gallery -----------------------------
branch = 'main'
link = f'https://github.com/pyfar/gallery/raw/{branch}/docs/'
folders_in = [
    '_static/css/custom.css',
    '_static/favicon.ico',
    '_static/header.rst',
    'resources/logos/pyfar_logos_fixed_size_imkar.png',
    ]

def download_files_from_gallery(link, folders_in):
    c = urllib3.PoolManager()
    for file in folders_in:
        url = link + file
        filename = file
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with c.request('GET', url, preload_content=False) as res:
            if res.status == 200:
                with open(filename, 'wb') as out_file:
                    shutil.copyfileobj(res, out_file)

download_files_from_gallery(link, folders_in)
# if logo does not exist, use pyfar logo
if not os.path.exists(html_logo):
    download_files_from_gallery(
        link, ['resources/logos/pyfar_logos_fixed_size_pyfar.png'])
    shutil.copyfile(
        'resources/logos/pyfar_logos_fixed_size_pyfar.png', html_logo)

# replace imkar hard link to internal link
with open("_static/header.rst", "rt") as fin:
    with open("header.rst", "wt") as fout:
        lines = [line.replace(f'https://{project}.readthedocs.io', project) for line in fin]
        contains_project = any(project in line for line in lines)

        fout.writelines(lines)

        # add project to the list of projects if not in header
        if not contains_project:
            fout.write(f'   {project} <{project}>\n')
        
        # count the number of gallery headings
        count_gallery_headings = np.sum(
            ['https://pyfar-gallery.readthedocs.io' in line for line in lines])


# set dropdown header after gallery headings
html_theme_options['header_links_before_dropdown'] = count_gallery_headings+1


