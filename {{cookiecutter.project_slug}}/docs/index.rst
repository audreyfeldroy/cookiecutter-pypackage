Welcome to {{ cookiecutter.project_name }}'s documentation!
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   readme
   installation
   usage
   modules
   {% if cookiecutter.open_source_license != 'Not open source' -%}contributing
   {% endif -%}
   {% if cookiecutter.create_author_file == 'y' -%}authors
   {% endif -%}history

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
