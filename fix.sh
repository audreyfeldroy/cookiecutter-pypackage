#!/bin/bash -eu

set -o pipefail

latest_version() {
  major_minor=${1}
  # https://stackoverflow.com/questions/369758/how-to-trim-whitespace-from-a-bash-variable
  pyenv install --list | grep "^  ${major_minor}." | grep -v -- -dev | tail -1 | xargs
}

install_pyenv() {
  if [ "$(uname)" == "Darwin" ]
  then
    HOMEBREW_NO_AUTO_UPDATE=1 brew install pyenv || true
    if ! type pyenv 2>/dev/null
    then
      # https://github.com/pyenv/pyenv-installer/blob/master/bin/pyenv-installer
      2>&1 cat <<EOF
WARNING: seems you still have not added 'pyenv' to the load path.

# Load pyenv automatically by adding
# the following to ~/.bashrc:

export PATH="/home/circleci/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
EOF
    fi
  else
    curl https://pyenv.run | bash
  fi
}

set_pyenv_env_variables() {
  # looks like pyenv scripts aren't -u clean:
  #
  # https://app.circleci.com/pipelines/github/apiology/cookiecutter-pypackage/15/workflows/10506069-7662-46bd-b915-2992db3f795b/jobs/15
  set +u
  export PATH="${HOME}/.pyenv/bin:$PATH"
  eval "$(pyenv init -)"
  eval "$(pyenv virtualenv-init -)"
  set -u
}

ensure_pyenv() {
  if ! type pyenv >/dev/null 2>&1 && ! [ -f "${HOME}/.pyenv/bin/pyenv" ]
  then
    install_pyenv
  fi

  if ! type pyenv >/dev/null 2>&1
  then
    set_pyenv_env_variables
  fi
}

ensure_pyenv

# You can find out which feature versions are still supported / have
# been release here: https://www.python.org/downloads/
python_versions="$(latest_version 3.9) $(latest_version 3.8) $(latest_version 3.7) $(latest_version 3.6)"

echo "Latest Python versions: ${python_versions}"

for ver in $python_versions
do
  if [ "$(uname)" == Darwin ]
  then
    # https://teratail.com/questions/309663
    HOMEBREW_NO_AUTO_UPDATE=1 brew install zlib bzip2 || true

    pyenv_install() {
      CFLAGS="-I$(brew --prefix zlib)/include -I$(brew --prefix bzip2)/include" LDFLAGS="-L$(brew --prefix zlib)/lib -L$(brew --prefix bzip2)/lib" pyenv install --skip-existing "$@"
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

latest_python_version="$(cut -d' ' -f1 <<< "${python_versions}")"
virtualenv_name="cookiecutter-pypackage-${latest_python_version}"
pyenv virtualenv "${latest_python_version}" "${virtualenv_name}" || true
pyenv virtualenv mylibs || true
pyenv local "${virtualenv_name}" ${python_versions} mylibs
# Make sure we have a pip with the 20.3 resolver, and after the
# initial bugfix release
pip install 'pip>=20.3.1'
pip install -r requirements_dev.txt
pip install -e .
