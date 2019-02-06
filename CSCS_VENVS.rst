============================
Virtual Environments at CSCS
============================

Configuration
-------------

Add the following lines to your `.bashrc`::

  # Location where pipenv stores its virtual environments
  export PIPENV_CACHE_DIR=/scratch/<username>/.pipenvs
  
  # Use the following mirror to install pip packages when using pipenv
  export PIPENV_PYPI_MIRROR=???
  
  # Location where virtualenvwrapper stores its virtual environments
  export WORKON_HOME=/scratch/<username>/.virtualenvs
  
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

* directly use the script ``virtualenv`` (see `virtualenv`_), or
* the scripts provided by virtualenvwrapper (see `virtualenvwrapper`_)

Note that you need to ``source /usr/local/bin/virtualenvwrapper.sh`` 
before you can use the scripts of virtualenvwrapper.

In the following, we introduce the most important command using `pipenv`::

    # Create a virutal env for current project (execute the command in the 
    # root directory of the project)
    $ pipenv 
    
    # The same specifying the python version to use
    $ pipenv --python 3.7
    
    # Activate the virtual envorinment associated with the current project 
    # (executed in the root directory of the project). If no environment associated
    # with the project exists then a new one is created on the fly.
    $ pipenv shell
    
    # or specifying the Pyhon version
    $ pipenv shell --python 3.7
    
    # to leave the environment
    $ deactivate
    
    # Install a new package used by the library or the application
    $ pipenv install package1
    
    # Install a new package used for development (such as the debugger)
    $ pipenv install pdb --dev
    
    # Install all packages used by the library or application specified in the Pipfile
    $ pipenv install
    
    # Install all packages used for development specified in the Pipfile
    $ pipenv install --dev
    
    # Install all packages used by the library or the application specified in the 
    # requirements.txt file
    $ pipenv install -r requirements.txt
    
    # Install all packages used for development specified in the requirements_dev.txt file
    $ pipenv install -r requirements_dev.txt --dev
    
    # Rewrite the requirements.txt and the requirements_dev.txt file (needed to sync the 
    # content of the Pipfile with the requirements.txt and the requirements_dev.txt)
    $ pipenv lock -r > requirements.txt
    $ pipenv lock -r -d > requirements_dev.txt
    
    # Pinpoint the version of the installed packages to rebuild the exact the same
    # virtual environment on another machine or for another user
    $ pipenv lock
    
    # And to rebuild it
    $ pipenv install --ignore-pipfile
    
    # Check for security updates
    $ pipenv check

.. _`pipenv`: https://realpython.com/pipenv-guide/
.. _`virtualenv`: https://virtualenv.pypa.io/en/stable/userguide/
.. _`virtualenvwrapper`: https://virtualenvwrapper.readthedocs.io/en/latest/index.html
