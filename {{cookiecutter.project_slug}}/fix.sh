#!/bin/bash -eu

set -o pipefail

latest_version() {
  major_minor=${1}
  # https://stackoverflow.com/questions/369758/how-to-trim-whitespace-from-a-bash-variable
  pyenv install --list | grep "^  ${major_minor}." | grep -v -- -dev | tail -1 | xargs
}

# You can find out which feature versions are still supported / have
# been release here: https://www.python.org/downloads/
python_versions="$(latest_version 3.9) $(latest_version 3.8) $(latest_version 3.7) $(latest_version 3.6)"

echo "Latest Python versions: ${python_versions}"

for ver in $python_versions
do
  if [ "$(uname)" == Darwin ]
  then
    if ! [ -f /usr/local/opt/zlib/lib/libz.dylib ]
    then
      # https://teratail.com/questions/309663
      HOMEBREW_NO_AUTO_UPDATE=1 brew install zlib || true
    fi
    if ! [ -f /usr/local/opt/bzip2/bin/bzip2 ]
    then
      # https://teratail.com/questions/309663
      HOMEBREW_NO_AUTO_UPDATE=1 brew install bzip2 || true
    fi

    pyenv_install() {
      CFLAGS="-I/usr/local/opt/zlib/include -I/usr/local/opt/bzip2/include" LDFLAGS="-L/usr/local/opt/zlib/lib -L/usr/local/opt/bzip2/lib" pyenv install --skip-existing "$@"
    }

    major_minor="$(cut -d. -f1-2 <<<"${ver}")"
    if [ "${major_minor}" == 3.6 ]
    then
      pyenv_install --patch "${ver}" < <(curl -sSL https://github.com/python/cpython/commit/8ea6353.patch\?full_index=1)
    else
      pyenv_install "${ver}"
    fi
  else
    pyenv install -s "${ver}"
  fi
done

# assumes you have an existing pyenv named mylibs where your global
# stuff goes
latest_python_version="$(cut -d' ' -f1 <<< "${python_versions}")"
virtualenv_name="{{ cookiecutter.project_slug }}-${latest_python_version}"
pyenv virtualenv "${latest_python_version}" "${virtualenv_name}" || true
pyenv local "${virtualenv_name}" ${python_versions} mylibs
# Make sure we have a pip with the 20.3 resolver, and after the
# initial bugfix release
pip install 'pip>=20.3.1'
pip install -r requirements_dev.txt
pip install -e .
