##
# cli
#
# The cli image produces a container that runs the CLI tool in the package.
#
FROM python:3.6-slim-stretch as cli

ENV PATH=$PATH:/home/user/.local/bin \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIPENV_COLORBLIND=true \
    PIPENV_NOSPIN=true \
    PIP_NO_CACHE_DIR=off \
    PIP_USER=1

# Run as non root user (best practice)
WORKDIR /srv

# Run as a non-root user.
RUN useradd -ms /bin/bash user \
 && chown -R user:user /srv
USER user

# Install pipenv.
RUN python -m pip install --upgrade --user pipenv

# Copy required project files into the WORKDIR.
COPY --chown=user:user Pipfile* setup.py setup.cfg /srv/

# Create a dummy service directory for the dependency installation.
RUN mkdir -p /srv/{{cookiecutter.project_slug}}

# Install environment dependencies with Pipenv. If no lockfile is present, we skip it.
RUN test -f "./Pipfile.lock" && pipenv install --system --keep-outdated --ignore-pipfile || pipenv install --system --skip-lock

# Copy the project directory (https://github.com/moby/moby/issues/29211)
COPY --chown=user:user {{cookiecutter.project_slug}} /srv/{{cookiecutter.project_slug}}

# Copy the entrypoint files for booting the application.
COPY --chown=user:user docker-entrypoint.sh /srv/

# Set the command executed first when the container run
ENTRYPOINT ["./docker-entrypoint.sh"]


##
# dev
#
# The dev image installs development-level dependencies in the container and
# the project to be mounted in the container.
#
FROM cli as dev

# Install environment dependencies with Pipenv.
RUN pipenv install --system --dev --skip-lock

# Mount a volume at /srv so code can be changed on the fly
VOLUME /srv
