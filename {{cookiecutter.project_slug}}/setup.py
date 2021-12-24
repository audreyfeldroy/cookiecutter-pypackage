#!/usr/bin/env python
import os
from pathlib import Path
from setuptools import setup, find_packages

this_directory = Path(__file__).parent.absolute()
long_description = (this_directory / "README.rst").read_text()

about = {}
about_path = os.path.join(this_directory, '{{ cookiecutter.project_slug }}', "__about__.py")
try: 
    with open(about_path, "r", encoding="utf-8") as f:
        exec(f.read(), about)
except:
    print(about_path)
    print(__file__)
    raise FileNotFoundError(about_path)
def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

## workaround derived from: https://github.com/pypa/pip/issues/7645#issuecomment-578210649
requirements = parse_requirements(
    'requirements.txt',
)
## workaround derived from: https://github.com/pypa/pip/issues/7645#issuecomment-578210649
dev_requirements = parse_requirements(
    'requirements_dev.txt',
)

test_requirements = [{%- if cookiecutter.use_pytest == 'y' %}'pytest>=3', "pytest-cov",{%- endif %} ]

extras_requires = {
    "dev": dev_requirements,
    "test": test_requirements,
}

{%- set license_classifiers = {
    'MIT license': 'License :: OSI Approved :: MIT License',
    'BSD license': 'License :: OSI Approved :: BSD License',
    'ISC license': 'License :: OSI Approved :: ISC License (ISCL)',
    'Apache Software License 2.0': 'License :: OSI Approved :: Apache Software License',
    'GNU General Public License v3': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
} %}

setup(
    author=about.get('__author__'),
    author_email=about.get('__email__'),
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
{%- if cookiecutter.open_source_license in license_classifiers %}
        '{{ license_classifiers[cookiecutter.open_source_license] }}',
{%- endif %}
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description=about.get('__description__'),
    {%- if 'no' not in cookiecutter.command_line_interface|lower %}
    entry_points={
        'console_scripts': [
            '{{ cookiecutter.project_slug }}={{ cookiecutter.project_slug }}.cli:main',
        ],
    },
    {%- endif %}
    install_requires=requirements,
    extra_requires=extras_requires,
{%- if cookiecutter.open_source_license in license_classifiers %}
    license="{{ cookiecutter.open_source_license }}",
{%- endif %}
    long_description=long_description,
    include_package_data=True,
    keywords='{{ cookiecutter.project_slug }}',
    name='{{ cookiecutter.project_slug }}',
    packages=find_packages(include=['{{ cookiecutter.project_slug }}', '{{ cookiecutter.project_slug }}.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url=about.get('__url__'),
    version=about.get('__version__'),
    zip_safe=False,
)
