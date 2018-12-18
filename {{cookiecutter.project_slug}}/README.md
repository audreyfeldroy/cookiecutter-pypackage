# {{ cookiecutter.project_name }}

*{{ cookiecutter.project_short_description }}*

[![PyPi](https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg)](https://pypi.python.org/pypi/{{ cookiecutter.project_slug }})

[![Travis](https://img.shields.io/travis/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.svg)](https://travis-ci.org/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }})

[![ReadTheDocs](https://readthedocs.org/projects/{{ cookiecutter.project_slug | replace("_", "-") }}/badge/?version=latest)](https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io/en/latest/?badge=latest)

{% if cookiecutter.add_pyup_badge == 'y' %}
[![PyUp](https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/shield.svg)](https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/)
{% endif %}

---

**ToDo's:**

- [ ] Consider writing your README first.  Doing so helps you clarify your intent, focuses your project, and it is much more fun to write documentation at the beginning of a project than at the end of one, see:
  - [Readme Driven Development](http://tom.preston-werner.com/2010/08/23/readme-driven-development.html)
  - [GitHub Guides: Mastering Markdown](https://guides.github.com/features/mastering-markdown/)
- [ ] Ensure you put the [license and copyright header](./HEADER) at the top of all your source code files.
- [ ] Be mindful of the third-party materials you use and ensure you follow Cisco's policies for creating and sharing Cisco Sample Code.

---

## Motivation

Include a short description of the motivation behind the creation and maintenance of the project.  Explain **why** the project exists.

## Show Me!

What visual, if shown, clearly articulates the impact of what you have created?  In as concise a visualization as possible (code sample, CLI output, animated GIF, or screenshot) show what your project makes possible.

## Features

Include a succinct summary of the features/capabilities of your project.

- Feature 1
- Feature 2
- Feature 3

## Technologies & Frameworks Used

This is Cisco Sample Code!  What Cisco and third-party technologies are you working with?  Are you using a coding framework or software stack?  A simple list will set the context for your project.

**Cisco Products & Services:**

- Product
- Service

**Third-Party Products & Services:**

- Product
- Service

**Tools & Frameworks:**

- Framework 1
- Automation Tool 2

## Usage

If people like your project, they will want to use it.  Show them how.

## Installation

Provide a step-by-step series of examples and explanations for how to install your project and its dependencies.

## Documentation

Please check the project documentation at:

https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io

## Authors & Maintainers

Smart people responsible for the creation and maintenance of this project:

- {{ cookiecutter.full_name }} <{{ cookiecutter.email }}>

## Credits

The following resources were influential in the creation of this project:

- This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and a derivative of the[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.

## License

This project is licensed to you under the terms of the [Cisco SampleCode License](./LICENSE).
