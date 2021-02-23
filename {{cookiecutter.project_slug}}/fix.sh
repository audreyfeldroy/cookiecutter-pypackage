#!/bin/bash -eu

set -o pipefail

install_rbenv() {
  if [ "$(uname)" == "Darwin" ]
  then
    HOMEBREW_NO_AUTO_UPDATE=1 brew install rbenv || true
    if ! type rbenv 2>/dev/null
    then
      # https://github.com/pyenv/pyenv-installer/blob/master/bin/pyenv-installer
      >&2 cat <<EOF
WARNING: seems you still have not added 'rbenv' to the load path.

# Load rbenv automatically by adding
# the following to ~/.bashrc:

export PATH="$HOME/.rbenv/bin:$PATH"
eval "$(rbenv init -)"
EOF
    fi
  else
    git clone https://github.com/rbenv/rbenv.git ~/.rbenv
  fi
}

set_rbenv_env_variables() {
  export PATH="${HOME}/.rbenv/bin:$PATH"
  eval "$(rbenv init -)"
}

install_ruby_build() {
  if [ "$(uname)" == "Darwin" ]
  then
    HOMEBREW_NO_AUTO_UPDATE=1 brew install ruby-build || true
  else
    mkdir -p "$(rbenv root)"/plugins
    git clone https://github.com/rbenv/ruby-build.git "$(rbenv root)"/plugins/ruby-build
  fi
}

ensure_ruby_build() {
  if ! type ruby-build >/dev/null 2>&1 && ! [ -d "${HOME}/.rbenv/plugins/ruby-build" ]
  then
    install_ruby_build
  fi
}

ensure_rbenv() {
  if ! type rbenv >/dev/null 2>&1 && ! [ -f "${HOME}/.rbenv/bin/rbenv" ]
  then
    install_rbenv
  fi

  set_rbenv_env_variables

  ensure_ruby_build
}

ensure_ruby_version() {
  rbenv install -s "$(cat .ruby-version)"
}

ensure_bundle() {
  bundle --version >/dev/null 2>&1 || gem install bundler
  bundle install
}

latest_python_version() {
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
      >&2 cat <<EOF
WARNING: seems you still have not added 'pyenv' to the load path.

# Load pyenv automatically by adding
# the following to ~/.bashrc:

export PATH="$HOME/.pyenv/bin:$PATH"
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

# You can find out which feature versions are still supported / have
# been release here: https://www.python.org/downloads/
ensure_python_versions() {
  # You can find out which feature versions are still supported / have
  # been release here: https://www.python.org/downloads/
  python_versions="$(latest_python_version 3.9)"

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
}

ensure_pyenv_virtualenvs() {
  latest_python_version="$(cut -d' ' -f1 <<< "${python_versions}")"
  virtualenv_name="{{cookiecutter.project_slug}}-${latest_python_version}"
  pyenv virtualenv "${latest_python_version}" "${virtualenv_name}" || true
  # You can use this for your global stuff!
  pyenv virtualenv "${latest_python_version}" mylibs || true
  # shellcheck disable=SC2086
  pyenv local "${virtualenv_name}" ${python_versions} mylibs
}

ensure_pip() {
  # Make sure we have a pip with the 20.3 resolver, and after the
  # initial bugfix release
  pip install 'pip>=20.3.1'
}

ensure_python_requirements() {
  pip install -r requirements_dev.txt
}

install_shellcheck() {
  if [ "$(uname)" == "Darwin" ]
  then
    HOMEBREW_NO_AUTO_UPDATE=1 brew install shellcheck || true
  elif type apt-get >/dev/null 2>&1
  then
    sudo apt-get update -y
    sudo apt-get install shellcheck
  fi
}

ensure_shellcheck() {
  if ! type shellcheck >/dev/null 2>&1
  then
    install_shellcheck
  fi
}

ensure_rbenv

ensure_ruby_version

ensure_bundle

ensure_pyenv

ensure_python_versions

ensure_pyenv_virtualenvs

ensure_pip

ensure_python_requirements

ensure_shellcheck
