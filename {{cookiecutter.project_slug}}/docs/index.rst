Welcome to {{ cookiecutter.project_name }}'s documentation!
============================{% for _ in cookiecutter.project_name %}={% endfor %}

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   readme
   installation
   usage
   modules
   {% if cookiecutter.create_author_file == 'y' -%}authors
   {% endif -%}history

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
