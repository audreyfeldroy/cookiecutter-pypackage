from setuptools import setup

import {{ cookiecutter.repo_name }}

setup(
    name={{cookiecutter.repo_name}}.__name__,
    version={{cookiecutter.repo_name}}.__version__,
    description='{{cookiecutter.project_description}}',
    author='{{cookiecutter.name}}',
    author_email='{{cookiecutter.email}}',
    url={{cookiecutter.repo_name}}.__url__
    packages=[{{cookiecutter.repo_name}}.__name__],
    package_dir={'{{cookiecutter.repo_name}}': '{{cookiecutter.repo_name}}'},
    include_package_data=True,
    install_requires=[
    ],
    test_suite='nose.collector',
    license=open('LICENSE').read(),
)

