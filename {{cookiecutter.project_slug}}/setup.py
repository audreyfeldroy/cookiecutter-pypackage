#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import os

from setuptools import setup, find_packages

version = __import__('{{ cookiecutter.project_slug }}').__version__
here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

reqs = [line.strip() for line in open('requirements.txt')]

{%- set license_classifiers = {
    'Apache Software License 2.0': 'License :: OSI Approved :: Apache Software License',
    'MIT license': 'License :: OSI Approved :: MIT License',
    'BSD license': 'License :: OSI Approved :: BSD License',
    'ISC license': 'License :: OSI Approved :: ISC License (ISCL)',
    'GNU General Public License v3': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
} %}

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Natural Language :: English',
    "Programming Language :: Python :: 2",
    'Programming Language :: Python :: 2.7',
    # 'Programming Language :: Python :: 3',
    # 'Programming Language :: Python :: 3.6',
    'Topic :: Scientific/Engineering :: Atmospheric Science',
{%- if cookiecutter.open_source_license in license_classifiers %}
    '{{ license_classifiers[cookiecutter.open_source_license] }}',
{%- endif %}
]

setup(name='{{ cookiecutter.project_slug }}',
      version='{{ cookiecutter.version }}',
      description="{{ cookiecutter.project_short_description }}",
      long_description=README + '\n\n' + CHANGES,
      author="{{ cookiecutter.full_name.replace('\"', '\\\"') }}",
      author_email='{{ cookiecutter.email }}',
      url='https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}',
      classifiers=classifiers,
{%- if cookiecutter.open_source_license in license_classifiers %}
      license="{{ cookiecutter.open_source_license }}",
{%- endif %}
      keywords='wps pywps birdhouse {{ cookiecutter.project_slug }}',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='{{ cookiecutter.project_slug }}',
      install_requires=reqs,
      entry_points={
          'console_scripts': [
             '{{ cookiecutter.project_slug }}={{ cookiecutter.project_slug }}:main',
          ]},)
