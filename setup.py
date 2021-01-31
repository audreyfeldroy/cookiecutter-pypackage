#!/usr/bin/env python3

from distutils.core import setup
from distutils.cmd import Command
from typing import List, Tuple, Optional
import distutils
import subprocess


class QualityCommand(Command):
    quality_target: Optional[str]

    description = 'Run quality tools on source code'
    user_options: List[Tuple[str, Optional[str], str]] = []

    def initialize_options(self) -> None:
        pass

    def finalize_options(self) -> None:
        pass

    def run(self) -> None:
        """Run command."""
        command = ['overcommit', '--run']
        self.announce(
            'Running command: %s' % str(command),
            level=distutils.log.INFO)  # type: ignore
        subprocess.check_call(command)


setup(
    name='cookiecutter-pypackage',
    packages=[],
    version='0.1.0',
    description='Cookiecutter template for a Python package',
    author='Audrey Roy Greenfeld',
    license='BSD',
    author_email='aroy@alum.mit.edu',
    url='https://github.com/audreyr/cookiecutter-pypackage',
    keywords=['cookiecutter', 'template', 'package', ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development',
    ],
    cmdclass={
        'quality': QualityCommand,
    },
)
