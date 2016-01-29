#!/usr/bin/env python
#
# Copyright (c) {{year}} Unravel Analytics

# This should be only one line. If it must be multi-line, indent the second
# line onwards to keep the PKG-INFO file format intact.
"""{{cookiecutter.description}}
"""

from setuptools import setup, find_packages
import glob
import os.path


def project_path(*names):
    return os.path.join(os.path.dirname(__file__), *names)


setup(
    name='{{cookiecutter.project_slug}}',
    version='{{cookiecutter.version}}',

    install_requires=[
        'distribute',
        ],

    extras_require={
        'test': [
            'coverage',
            'mock',
            'nose',
            'tox',
            'unittests2',
        ],
    },
    test_suite='nose.collector',

    entry_points={
        # change script_name here to something that makes sense
        'console_scripts': ['script_name={{cookiecutter.project_slug}}.script_entry:first_script'],
    },
    url="",
    author='Unravel Analytics',
    author_email='development@unravel.ie',
    license='(c) Unravel Analytics, all rights reserved',
    classifiers="""\
Programming Language :: Python :: 2.7
Private :: Do Not Upload
"""[:-1].split('\n'),
    description=__doc__.strip(),
    long_description='\n\n'.join(open(project_path(name)).read() for name in (
            'README.md',
            )),

    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    data_files=[('', glob.glob(project_path('*.txt')), glob.glob(project_path('*.rst')))],
    zip_safe=False,
    )
