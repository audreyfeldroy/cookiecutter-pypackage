Project
-------

- [ ] Fork the `original project <https://cookiecutter-pypackage.readthedocs.io/en/latest/tutorial.html>`_ rather than Nekroze's

Process
-------

- [ ] Allow the \'-\' in the project & repository names : cf hooks/pre
- [ ] Distinguish the project / repository / module names : cf cookiecutter.json
- [ ] Remove the publish part (to pypi)

Data
----

- [ ] Connect the template to `Airflow <https://pythonhosted.org/airflow/tutorial.html>`_
- [ ] Prompt the user for data :
        - origin
        - format

Add the new parameters to cookiecutter.json

Environment
-----------

- [ ] Use pipenv :
        - in the make recipes
        - install all the dev packages with \'make init\'
