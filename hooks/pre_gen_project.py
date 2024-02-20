import re
import sys

from packaging import version

MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

module_name = '{{ cookiecutter.project_slug}}'

if not re.match(MODULE_REGEX, module_name):
    print('ERROR: The project slug (%s) is not a valid Python module name. Please do not use a - and use _ instead' % module_name)

    #Exit to cancel project
    sys.exit(1)


MODULE_REGEX = '3.[0-9]+'
default_python_version = '{{ cookiecutter.default_python_version }}'
if not re.match(MODULE_REGEX, default_python_version):
    print('ERROR: The project slug (%s) is not a valid Python version number. Please use python 3.x' % default_python_version)

    #Exit to cancel project
    sys.exit(1)


MODULE_REGEX = '3.[0-9]+'
minimum_python_version = '{{ cookiecutter.minimum_python_version }}'
if not re.match(MODULE_REGEX, minimum_python_version):
    print('ERROR: The project slug (%s) is not a valid Python version number. Please use python 3.x' % minimum_python_version)

    #Exit to cancel project
    sys.exit(1)


if version.parse(default_python_version) < version.parse(minimum_python_version):
    print(f'ERROR: The default python version ({default_python_version}) is not greater or equal than the minimum python version ({minimum_python_version}). Please use a default python version greater or equal than the minimum python version')

    #Exit to cancel project
    sys.exit(1)

