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

latest_ruby_version() {
  major_minor=${1}
  rbenv install --list 2>/dev/null | grep "^${major_minor}."
}

ensure_dev_library() {
  header_file_name=${1:?header file name}
  homebrew_package=${2:?homebrew package}
  apt_package=${3:-${homebrew_package}}
  if ! [ -f /usr/include/"${header_file_name}" ] && \
      ! [ -f /usr/include/x86_64-linux-gnu/"${header_file_name}" ] && \
      ! [ -f /usr/local/include/"${header_file_name}" ] && \
      ! [ -f  /usr/local/opt/"${homebrew_package}"/include/"${header_file_name}" ]
  then
    install_package "${homebrew_package}" "${apt_package}"
  fi
}

ensure_ruby_build_requirements() {
  ensure_dev_library readline/readline.h readline libreadline-dev
}

# You can find out which feature versions are still supported / have
# been release here: https://www.ruby-lang.org/en/downloads/
ensure_ruby_versions() {
  # You can find out which feature versions are still supported / have
  # been release here: https://www.python.org/downloads/
  ruby_versions="$(latest_ruby_version 3.0)"

  echo "Latest Ruby versions: ${ruby_versions}"

  ensure_ruby_build_requirements

  for ver in $ruby_versions
  do
    rbenv install -s "${ver}"
  done
}

ensure_bundle() {
  bundle --version >/dev/null 2>&1 || gem install bundler
  bundle install
  # https://bundler.io/v2.0/bundle_lock.html#SUPPORTING-OTHER-PLATFORMS
  #
  # "If you want your bundle to support platforms other than the one
  # you're running locally, you can run bundle lock --add-platform
  # PLATFORM to add PLATFORM to the lockfile, force bundler to
  # re-resolve and consider the new platform when picking gems, all
  # without needing to have a machine that matches PLATFORM handy to
  # install those platform-specific gems on.'
  bundle lock --add-platform x86_64-darwin-20 x86_64-linux
}

set_ruby_local_version() {
  latest_ruby_version="$(cut -d' ' -f1 <<< "${ruby_versions}")"
  echo "${latest_ruby_version}" > .ruby-version
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

install_package() {
  homebrew_package=${1:?homebrew package}
  apt_package=${2:-${homebrew_package}}
  if [ "$(uname)" == "Darwin" ]
  then
    HOMEBREW_NO_AUTO_UPDATE=1 brew install "${homebrew_package}"
  elif type apt-get >/dev/null 2>&1
  then
    sudo apt-get update -y
    sudo apt-get install -y "${apt_package}"
  else
    >&2 echo "Teach me how to install packages on this plaform"
    exit 1
  fi
}

ensure_python_build_requirements() {
  ensure_dev_library zlib.h zlib zlib1g-dev
  ensure_dev_library bzlib.h bzip2 libbz2-dev
  ensure_dev_library openssl/ssl.h openssl libssl-dev
  ensure_dev_library ffi.h libffi libffi-dev
}

# You can find out which feature versions are still supported / have
# been release here: https://www.python.org/downloads/
ensure_python_versions() {
  # You can find out which feature versions are still supported / have
  # been release here: https://www.python.org/downloads/
  python_versions="$(latest_python_version 3.9)"

  echo "Latest Python versions: ${python_versions}"

  ensure_python_build_requirements

  for ver in $python_versions
  do
    if [ "$(uname)" == Darwin ]
    then
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

ensure_shellcheck() {
  if ! type shellcheck >/dev/null 2>&1
  then
    install_package shellcheck
  fi
}

ensure_rbenv

ensure_ruby_versions

set_ruby_local_version

ensure_bundle

ensure_pyenv

ensure_python_versions

ensure_pyenv_virtualenvs

ensure_pip

ensure_python_requirements

ensure_shellcheck
