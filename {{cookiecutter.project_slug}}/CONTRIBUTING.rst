{% set rwth = cookiecutter.git_service == 'https://git.rwth-aachen.de' -%}
{% set github = cookiecutter.git_service == 'https://github.com' -%}
.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

Types of Contributions
----------------------

Report Bugs or Suggest Features
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The best place for this is {{ cookiecutter.git_service }}/{{ cookiecutter.git_username }}/{{ cookiecutter.project_slug }}/issues.

Fix Bugs or Implement Features
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Look through {{ cookiecutter.git_service }}/{{ cookiecutter.git_username }}/{{ cookiecutter.project_slug }}/issues for bugs or feature request
and contact us or comment if you are interested in implementing.

Write Documentation
~~~~~~~~~~~~~~~~~~~

{{ cookiecutter.project_slug }} could always use more documentation, whether as part of the
official {{ cookiecutter.project_slug }} docs, in docstrings, or even on the web in blog posts,
articles, and such.

Get Started!
------------

Ready to contribute? Here's how to set up `{{ cookiecutter.project_slug }}` for local development using the command-line interface. Note that several alternative user interfaces exist, e.g., the Git GUI, `GitHub Desktop <https://desktop.github.com/>`_, extensions in `Visual Studio Code <https://code.visualstudio.com/>`_ ...

1. `Fork <https://docs.github.com/en/get-started/quickstart/fork-a-repo/>`_ the `{{ cookiecutter.project_slug }}` repo on GitHub.
2. Clone your fork locally and cd into the {{ cookiecutter.project_slug }} directory::

    $ git clone https://github.com/YOUR_USERNAME/{{ cookiecutter.project_slug }}.git
    $ cd {{ cookiecutter.project_slug }}

3. Install your local copy into a virtualenv. Assuming you have Anaconda or Miniconda installed, this is how you set up your fork for local development::

    $ conda create --name {{ cookiecutter.project_slug }} python
    $ conda activate {{ cookiecutter.project_slug }}
    $ conda install pip
    $ pip install -e .
    $ pip install -r requirements_dev.txt

4. Create a branch for local development. Indicate the intention of your branch in its respective name (i.e. `feature/branch-name` or `bugfix/branch-name`)::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests::

    $ flake8 {{ cookiecutter.project_slug }} tests
    $ pytest

   flake8 test must pass without any warnings for `./{{ cookiecutter.project_slug }}` and `./tests` using the default or a stricter configuration. Flake8 ignores `E123/E133, E226` and `E241/E242` by default. If necessary adjust your flake8 and linting configuration in your IDE accordingly.

6. Commit your changes and push your branch to {% if rwth %}GitLab{% elif github %}GitHub{% endif %}::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request on the develop branch through the {% if rwth %}GitLab{% elif github %}GitHub{% endif %} website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring.
3. If checks do not pass, have a look at https://app.circleci.com/pipelines/github/{{ cookiecutter.git_username }}/{{ cookiecutter.project_slug }} for more information.

Function and Class Guidelines
-----------------------------

Functions and classes should

* have a single clear purpose and a functionality limited to that purpose. Conditional parameters are fine in some cases but are an indicator that a function or class does not have a clear purpose. Conditional parameters are

  - parameters that are obsolete if another parameter is provided
  - parameters that are necessary only if another parameter is provided
  - parameters that must have a specific value depending on other parameters

* be split into multiple functions or classes if the functionality not well limited.
* contain documentation for all input and output parameters.
* contain examples in the documentation if they are non-trivial to use.
* contain comments in the code that explain decisions and parts that are not trivial to read from the code. As a rule of thumb, too much comments are better than to little comments.
* use clear names for all variables

It is also a good idea to follow `the Zen of Python <https://peps.python.org/pep-0020/>`_

Errors should be raised if

* Audio objects do not have the correct type (e.g. a TimeData instance is passed but a Signal instance is required)
* String input that specifies a function option has an invalid value (e.g. 'linea' was passed but 'linear' was required)
* Invalid parameter combinations are used

Warnings should be raised if

* Results might be wrong or unexpected
* Possibly bad parameter combinations are used


Testing Guidelines
-----------------------
Pyfar uses test-driven development based on `three steps <https://martinfowler.com/bliki/TestDrivenDevelopment.html>`_ and `continuous integration <https://en.wikipedia.org/wiki/Continuous_integration>`_ to test and monitor the code.
In the following, you'll find a guideline. Note: these instructions are not generally applicable outside of pyfar.

- The main tool used for testing is `pytest <https://docs.pytest.org/en/stable/index.html>`_.
- All tests are located in the *tests/* folder.
- Make sure that all important parts of {{ cookiecutter.project_slug }} are covered by the tests. This can be checked using *coverage* (see below).
- In case of {{ cookiecutter.project_slug }}, mainly **state verification** is applied in the tests. This means that the outcome of a function is compared to a desired value (``assert ...``). For more information, it is refered to `Martin Fowler's article <https://martinfowler.com/articles/mocksArentStubs.html.>`_.

Required Tests
~~~~~~~~~~~~~~

The testing should include

- Test all errors and warnings (see also function and class guidelines above)
- Test all parameters
- Test specific parameter combinations if required
- Test with single and multi-dimensional input data such Signal objects and array likes
- Test with audio objects with complex time data and NaN values (if applicable)

Tips
~~~~~~~~~~~
Pytest provides several, sophisticated functionalities which could reduce the effort of implementing tests.

- Similar tests executing the same code with different variables can be `parametrized <https://docs.pytest.org/en/stable/example/parametrize.html>`_. An example is ``test___eq___differInPoints`` in *test_coordinates.py*.

- Run a single test with

    $ pytest tests/test_plot.py::test_line_plots

- Exclude tests (for example the time consuming test of plot) with

    $ pytest -k 'not plot and not interaction'

- Create an html report on the test `coverage <https://coverage.readthedocs.io/en/coverage-5.5/>`_ with

    $ pytest --cov=. --cov-report=html

- Feel free to add more recommendations on useful pytest functionalities here. Consider, that a trade-off between easy implemention and good readability of the tests needs to be found.

Fixtures
~~~~~~~~
"Software test fixtures initialize test functions. They provide a fixed baseline so that tests execute reliably and produce consistent, repeatable, results. Initialization may setup services, state, or other operating environments. These are accessed by test functions through parameters; for each fixture used by a test function there is typically a parameter (named after the fixture) in the test function’s definition." (from https://docs.pytest.org/en/stable/fixture.html)

- All fixtures are implemented in *conftest.py*, which makes them automatically available to all tests. This prevents from implementing redundant, unreliable code in several test files.
- Typical fixtures are {{ cookiecutter.project_slug }} objects with varying properties, stubs as well as functions need for initiliazing tests.
- Define the variables used in the tests only once, either in the test itself or in the definition of the fixture. This assures consistency and prevents from failing tests due to the definition of variables with the same purpose at different positions or in different files.

Have a look at already implemented fixtures in *confest.py*.

**Dummies**

If the objects used in the tests have arbitrary properties, tests are usually better to read, when these objects are initialized within the tests. If the initialization requires several operations or the object has non-arbitrary properties, this is a hint to use a fixture.
Good examples illustrating these two cases are the initializations in *test_signal.py* vs. the sine and impulse signal fixtures in *conftest.py*.

**Stubs**

Stubs mimic actual objects, but have minimum functionality and **fixed, well defined properties**. They are **only used in cases, when a dependence on the actual {{ cookiecutter.project_slug }} class is prohibited**. This is the case, when functionalities of the class itself or methods it depends on are tested. Examples are the tests of the Signal class and its methods in *test_signal.py* and *test_fft.py*.

It requires a little more effort to implement stubs of the {{ cookiecutter.project_slug }} classes. Therefore, stub utilities are provided in *{{ cookiecutter.project_slug }}/testing/stub_utils.py* and imported in *confest.py*, where the actual stubs are implemented.

- Note: the stub utilities are not meant to be imported to test files directly or used for other purposes than testing. They solely provide functionality to create fixtures.
- The utilities simplify and harmonize testing within the {{ cookiecutter.project_slug }} package and improve the readability and reliability.
- The implementation as the private submodule ``{{ cookiecutter.project_slug }}.testing.stub_utils``  further allows the use of similar stubs in related packages with {{ cookiecutter.project_slug }} dependency (e.g. other packages from the pyfar family).

**Mocks**

Mocks are similar to stubs but used for **behavioral verification**. For example, a mock can replace a function or an object to check if it is called with correct parameters. A main motivation for using mocks is to avoid complex or time-consuming external dependencies, for example database queries.

- A typical use case of mocks in the {{ cookiecutter.project_slug }} context is hardware communication, for example reading and writing of large files or audio in- and output. These use cases are rare compared to tests performing state verification.
- In contrast to some other guidelines on mocks, external dependencies do **not** need to be mocked in general. Failing tests due to changes in external packages are meaningful hints to modify the code.
- Examples of internal mocking can be found in *test_io.py*, indicated by the pytest ``@patch`` calls.


Writing the Documentation
-------------------------

Pyfar follows the `numpy style guide <https://numpydoc.readthedocs.io/en/latest/format.html>`_ for the docstring. A docstring has to consist at least of

- A short and/or extended summary,
- the Parameters section, and
- the Returns section

Optional fields that are often used are

- References,
- Examples, and
- Notes

Here are a few tips to make things run smoothly

- Use the tags ``:py:func:``, ``:py:mod:``, and ``:py:class:`` to reference pyfar functions, modules, and classes: For example ``:py:func:`~pyfar.plot.time``` for a link that displays only the function name. For links with custom text use ``:py:mod:`plot functions <pyfar.plot>```.
- Code snippets and values as well as external modules, classes, functions are marked by double ticks \`\` to appear in mono spaced font, e.g., ``x=3`` or ``pyfar.Signal``.
- Parameters, returns, and attributes are marked by single ticks \` to appear as emphasized text, e.g., *unit*.
- Use ``[#]_`` and ``.. [#]`` to get automatically numbered footnotes.
- Do not use footnotes in the short summary. Only use footnotes in the extended summary if there is a short summary. Otherwise, it messes with the auto-footnotes.
- If a method or class takes or returns pyfar objects for example write ``parameter_name : Signal``. This will create a link to the ``pyfar.Signal`` class.
- Plots can be included in the documentation by using the prefix ``.. plot::`` followed by an empty line and an indented block containing the code for the plot. See `pyfar.plot.line.time.py` for examples.

See the `Sphinx homepage <https://www.sphinx-doc.org>`_ for more information.

Building the Documentation
--------------------------

You can build the documentation of your branch using Sphinx by executing the make script inside the docs folder.

.. code-block:: console

    $ cd docs/
    $ make html

After Sphinx finishes you can open the generated html using any browser

.. code-block:: console

    $ docs/_build/index.html

Note that some warnings are only shown the first time you build the
documentation. To show the warnings again use

.. code-block:: console

    $ make clean

before building the documentation.


Deploying
~~~~~~~~~

A reminder for the maintainers on how to deploy.

- Commit all changes to develop
- Check if gallery needs to be updated
- Update HISTORY.rst in develop
- Merge develop into main

Switch to main and run::

$ bumpversion patch # possible: major / minor / patch
$ git push --follow-tags

The testing platform will then deploy to PyPI if tests pass.

- merge main back into develop
