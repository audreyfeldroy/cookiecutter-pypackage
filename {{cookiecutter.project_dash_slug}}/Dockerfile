##
# base
#
# The base image is the common part of src and tagged:
# both allow running the CLI tool,
# they also both allow running the test suite
# (requiring pipenv install --system --dev --skip-lock).
# The image contains the environment variables needed
# to complete code climate's coverage report.
#
FROM python:3.7-slim-stretch as base

ENV PATH=$PATH:/home/user/.local/bin \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIPENV_COLORBLIND=true \
    PIPENV_NOSPIN=true \
    PIP_NO_CACHE_DIR=off \
    PIP_USER=1

WORKDIR /srv

# Run as a non-root user.
RUN useradd -ms /bin/bash user \
 && chown -R user:user /srv
USER user

# Install the newest pip
RUN python -m pip install --upgrade --user pipenv

# Copy the entrypoint files for booting the application.
COPY --chown=user:user docker-entrypoint.sh /srv/

# Copy test configuration(s)
COPY --chown=user:user .coveragerc /srv/.coveragerc

# Copy the test suite
COPY --chown=user:user tests /srv/tests

# Copy bin scripts locally
COPY --chown=user:user bin /srv/bin

# Set the command executed first when the container run
ENTRYPOINT ["./docker-entrypoint.sh"]

##
# tagged
#
# The tagged image produces a container that runs the CLI tool in the package,
# using the specified version of the python package.
# The Pipfile.lock has to have no local dependencies.
#

FROM base as tagged

# Allow
ARG tag=

COPY --chown=user:user Pipfile Pipfile.lock /srv/
RUN if test -n "$tag"; then pipenv install --system ; fi

##
# src
#
# The src image produces a container that runs the CLI tool in the package.
#

FROM base as src

# Copy required project files into the WORKDIR.
COPY --chown=user:user Pipfile* setup.py setup.cfg /srv/

# Install environment dependencies with Pipenv. If no lockfile is present, we skip it.
RUN test -f "./Pipfile.lock" && pipenv install --system --keep-outdated --ignore-pipfile || pipenv install --system --skip-lock

# Copy the project directory (https://github.com/moby/moby/issues/29211)
COPY --chown=user:user  {{cookiecutter.project_slug}} /srv/{{cookiecutter.project_slug}}

##
# dev
#
# The dev image installs development-level dependencies in the container and
# the project to be mounted in the container.
#
FROM src as dev

# Install environment dependencies with Pipenv.
RUN pipenv install --system --dev --skip-lock

# Mount a volume at /srv so code can be changed on the fly
VOLUME /srv

##
# test
#
# The `test` image provides a dedicated container for running the application
# test suite. It is based on the `src` image so that a developer will have
# diagnostic tools available in the event of a failure.
#
FROM src as test

# Copy bin scripts locally
COPY --chown=user:user bin /srv/bin

# Copy test configuration(s)
COPY --chown=user:user .coveragerc /srv/.coveragerc

# Install testing dependencies with Pipenv.
RUN pipenv install --system --dev --skip-lock

# Install the test reporter for code climate
ENV CC_REPORTER_URL=https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64
ADD --chown=user:user "$CC_REPORTER_URL" /srv/cc-test-reporter
