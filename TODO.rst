####
TODO
####

Project
-------

- [ ] Fork the `original project <https://cookiecutter-pypackage.readthedocs.io/en/latest/tutorial.html>`_ rather than Nekroze's

Process
-------

- [x] Allow the \'-\' in the project & repository names : cf hooks/pre
- [x] Distinguish the project / repository / module names : cf cookiecutter.json
- [x] Remove the publish part (to pypi)

Data
----

- [ ] Connect the template to `Airflow <https://pythonhosted.org/airflow/tutorial.html>`_
- [ ] Prompt the user for data :
        - origin
        - format

Add the new parameters to cookiecutter.json

Environment
-----------

- [x] Use pipenv :
        - in the make recipes
        - install all the dev packages with \'make init\'
- [ ] configure with a given Python version :
  - [ ] tests : tox & py.test
  - [ ] pipenv (--two --three or --python xxx)

Installation
------------

- [ ] factor the dependencies, spread in the files :
  - requirements.txt
  - requirements_dev.txt
  - setup.py
