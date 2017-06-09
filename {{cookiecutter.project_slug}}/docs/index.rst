.. python_boilerplate documentation master file, created by
   sphinx-quickstart on Fri Jun  9 13:47:02 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to {{ cookiecutter.project_name }}'s documentation!
==============================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   readme
   installation
   usage
   contributing
   {% if cookiecutter.create_author_file == 'y' -%}authors
   {% endif -%}history


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
