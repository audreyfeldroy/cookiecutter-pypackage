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
sys.path.insert(0, os.path.abspath('..'))

import {{ cookiecutter.project_slug }}

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
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = '{{ cookiecutter.project_name }}'
copyright = "{% now 'local', '%Y' %}, {{ cookiecutter.full_name }}"
author = "{{ cookiecutter.full_name }}"

# The version info for the project you're documenting, acts as replacement
# for |version| and |release|, also used in various other places throughout
# the built documents.
#
# The short X.Y version.
version = {{ cookiecutter.project_slug }}.__version__
# The full version, including alpha/beta/rc tags.
release = {{ cookiecutter.project_slug }}.__version__

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
{% if cookiecutter.use_numpy == 'y' -%}
    'numpy': ('https://numpy.org/doc/stable/', None),{% endif %}
{% if cookiecutter.use_scipy == 'y' -%}
    'scipy': ('https://docs.scipy.org/doc/scipy/', None),{% endif %}
{% if cookiecutter.use_matplotlib == 'y' -%}
    'matplotlib': ('https://matplotlib.org/stable/', None),{% endif %}
{% if cookiecutter.use_pyfar == 'y' -%}
    'pyfar': ('https://pyfar.readthedocs.io/en/stable/', None),{% endif %}
    }

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_css_files = ['css/custom.css']
html_logo = '{{ cookiecutter.logo_path_gallery }}'
html_title = "{{ cookiecutter.project_slug }}"
html_favicon = '_static/favicon.ico'

# -- HTML theme options
# https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/layout.html

html_theme_options = {
    "navbar_start": ["navbar-logo"],
    "navbar_end": ["navbar-icon-links", "theme-switcher"],
    "navbar_align": "content",
    "header_links_before_dropdown": 8,
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
}

html_context = {
   "default_mode": "light"
}

# redirect index to pyfar.html
redirects = {
     "index": "{{ cookiecutter.project_slug }}.html"
}

# -- download navbar and style files from gallery -----------------------------
branch = 'main'
link = f'https://github.com/pyfar/gallery/raw/{branch}/docs/'
folders_in = [
    '_static/css/custom.css',
    '_static/favicon.ico',
    '_static/header.rst',
    '{{ cookiecutter.logo_path_gallery }}',
    ]
c = urllib3.PoolManager()
for file in folders_in:
    url = link + file
    filename = file
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with c.request('GET', url, preload_content=False) as res, open(filename, 'wb') as out_file:
        shutil.copyfileobj(res, out_file)

# replace pyfar hard link to internal link
with open("_static/header.rst", "rt") as fin:
    with open("header.rst", "wt") as fout:
        for line in fin:
            fout.write(line.replace(f'https://{project}.readthedocs.io', project))
