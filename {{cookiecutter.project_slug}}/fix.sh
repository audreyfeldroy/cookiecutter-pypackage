#!/bin/bash -eu

set -o pipefail

apt_upgraded=0

update_apt() {
  if [ "${apt_upgraded}" = 0 ]
  then
    sudo DEBIAN_FRONTEND=noninteractive apt-get update -y
    apt_upgraded=1
  fi
}

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
  ensure_dev_library zlib.h zlib zlib1g-dev
  ensure_dev_library openssl/ssl.h openssl libssl-dev
}

# You can find out which feature versions are still supported / have
# been release here: https://www.ruby-lang.org/en/downloads/
ensure_ruby_versions() {
  # You can find out which feature versions are still supported / have
  # been release here: https://www.ruby-lang.org/en/downloads/
  ruby_versions="$(latest_ruby_version 3.0)"

  echo "Latest Ruby versions: ${ruby_versions}"

  ensure_ruby_build_requirements

  for ver in $ruby_versions
  do
    # These CFLAGS can be retired once 2.6.7 is no longer needed :
    #
    # https://github.com/rbenv/ruby-build/issues/1747
    # https://github.com/rbenv/ruby-build/issues/1489
    # https://bugs.ruby-lang.org/issues/17777
    if [ "${ver}" == 2.6.7 ]
    then
      CFLAGS="-Wno-error=implicit-function-declaration" rbenv install -s "${ver}"
    else
      rbenv install -s "${ver}"
    fi
  done
}

ensure_bundle() {
  # Not sure why this is needed a second time, but it seems to be?
  #
  # https://app.circleci.com/pipelines/github/apiology/source_finder/21/workflows/88db659f-a4f4-4751-abc0-46f5929d8e58/jobs/107
  set_rbenv_env_variables
  bundle --version >/dev/null 2>&1 || gem install --no-document bundler
  bundler_version=$(bundle --version | cut -d ' ' -f3)
  bundler_version_major=$(cut -d. -f1 <<< "${bundler_version}")
  bundler_version_minor=$(cut -d. -f2 <<< "${bundler_version}")
  bundler_version_patch=$(cut -d. -f3 <<< "${bundler_version}")
  # Version 2.1 of bundler seems to have some issues with nokogiri:
  #
  # https://app.asana.com/0/1107901397356088/1199504270687298

  # Version 2.2.22 of bundler comes with a fix to ensure the 'bundle
  # update --conservative' flag works as expected - important when
  # doing a 'bundle update' on a about-to-be-published gem after
  # bumping a gem version.
  need_better_bundler=false
  if [ "${bundler_version_major}" -lt 2 ]
  then
    need_better_bundler=true
  elif [ "${bundler_version_major}" -eq 2 ]
  then
    if [ "${bundler_version_minor}" -lt 2 ]
    then
      need_better_bundler=true
    elif [ "${bundler_version_minor}" -eq 2 ]
    then
      if [ "${bundler_version_patch}" -lt 22 ]
      then
        need_better_bundler=true
      fi
    fi
  fi
  if [ "${need_better_bundler}" = true ]
  then
    gem install --no-document bundler
  fi
  make bundle_install
  # https://bundler.io/v2.0/bundle_lock.html#SUPPORTING-OTHER-PLATFORMS
  #
  # "If you want your bundle to support platforms other than the one
  # you're running locally, you can run bundle lock --add-platform
  # PLATFORM to add PLATFORM to the lockfile, force bundler to
  # re-resolve and consider the new platform when picking gems, all
  # without needing to have a machine that matches PLATFORM handy to
  # install those platform-specific gems on.'
  #
  # This affects nokogiri, which will try to reinstall itself in
  # Docker builds where it's already installed if this is not run.
  for platform in x86_64-darwin-20 x86_64-linux
  do
    grep "${platform:?}" Gemfile.lock >/dev/null 2>&1 || bundle lock --add-platform "${platform:?}"
  done
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

export PYENV_ROOT="${HOME}/.pyenv"
export PATH="${PYENV_ROOT}/bin:$PATH"
eval "$(pyenv init --path)"
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
  export PYENV_ROOT="${HOME}/.pyenv"
  export PATH="${PYENV_ROOT}/bin:$PATH"
  eval "$(pyenv init --path)"
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
    update_apt
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y "${apt_package}"
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
  ensure_dev_library sqlite3.h sqlite3 libsqlite3-dev
  ensure_dev_library lzma.h xz liblzma-dev
  ensure_dev_library readline/readline.h readline libreadline-dev
}

# You can find out which feature versions are still supported / have
# been release here: https://www.python.org/downloads/
ensure_python_versions() {
  # You can find out which feature versions are still supported / have
  # been release here: https://www.python.org/downloads/
  python_versions="$(latest_python_version 3.10)"

  echo "Latest Python versions: ${python_versions}"

  ensure_python_build_requirements

  for ver in $python_versions
  do
    if [ "$(uname)" == Darwin ]
    then
      if [ -z "${HOMEBREW_OPENSSL_PREFIX:-}" ]
      then
        HOMEBREW_OPENSSL_PREFIX="$(brew --prefix openssl)"
      fi
      pyenv_install() {
        CFLAGS="-I/usr/local/opt/zlib/include -I/usr/local/opt/bzip2/include -I${HOMEBREW_OPENSSL_PREFIX}/include" LDFLAGS="-L/usr/local/opt/zlib/lib -L/usr/local/opt/bzip2/lib -L${HOMEBREW_OPENSSL_PREFIX}/lib" pyenv install --skip-existing "$@"
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

ensure_pip_and_wheel() {
  # Make sure we have a pip with the 20.3 resolver, and after the
  # initial bugfix release
  major_pip_version=$(pip --version | cut -d' ' -f2 | cut -d '.' -f 1)
  if [[ major_pip_version -lt 21 ]]
  then
    pip install 'pip>=20.3.1'
  fi
  # wheel is helpful for being able to cache long package builds
  pip show wheel >/dev/null 2>&1 || pip install wheel
}

ensure_python_requirements() {
  make pip_install
}

ensure_shellcheck() {
  if ! type shellcheck >/dev/null 2>&1
  then
    install_package shellcheck
  fi
}

ensure_overcommit() {
  # don't run if we're in the middle of a cookiecutter child project
  # test, or otherwise don't have a Git repo to install hooks into...
  if [ -d .git ]
  then
    bundle exec overcommit --install
  else
    >&2 echo 'Not in a git repo; not installing git hooks'
  fi
}

ensure_rbenv

ensure_ruby_versions

set_ruby_local_version

ensure_bundle

ensure_pyenv

ensure_python_versions

ensure_pyenv_virtualenvs

ensure_pip_and_wheel

ensure_python_requirements

ensure_shellcheck

ensure_overcommit
