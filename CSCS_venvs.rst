============================
Virtual Environments at CSCS
============================

Configuration
-------------

Add the following lines to your `.bashrc`::

  # Location where pipenv stores its virtual environments
  PIPENV_CACHE_DIR=/scratch/<username>/.venvs
  
  # Use the following mirror to install pip packages when using pipenv
  PIPENV_PYPI_MIRROR=???
  
  # Location where virtualenvwrapper stores its virtual environments
  WORKON_HOME=/scratch/<username>/.envs
  
Add the file ``.pypirc`` to your home directory with the following content::

  # Pip donwnload configuration
  
  [global]
  # index = https://nexus.meteoswiss.ch/repository/python-all/pypi
  # index-url = https://nexus.meteoswiss.ch/repository/python-all/simple
  
  # List packages in column format
  [list]
  format = columns
  
Using Virtual Environments
--------------------------

Scripts and programs to manage virtual environments are provided by the
Python module. To load it, execute the following command::

  $ module load python[/<version>]
  
To manage virtual environments, we recommand to use the script ``pipenv`` 
(for further documentation see `pipenv`_). Other possiblities to manage virtual
environments are

* direclty use the script ``virtualenv`` (see `virtualenv`_), or
* the scripts provided by virtualenvwrapper (see `virtualenvwrapper`_)

Note that you need to ``source <file>`` before you can use the scripts of virtualenvwrapper.



.. _`pipenv`: https://realpython.com/pipenv-guide/
.. _`virtualenv`: https://virtualenv.pypa.io/en/stable/userguide/
.. _`virtualenvwrapper`: https://virtualenvwrapper.readthedocs.io/en/latest/index.html
