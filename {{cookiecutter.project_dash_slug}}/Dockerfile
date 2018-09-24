# Base Image
FROM python:3.6-slim-stretch

# Best practice: if you build contains several layers you should order them
# from the less frequently changed to the more frequently changed (caching)

# Install tools required for the project
# Best practice:
# 1. do not install unnecessary packages, keep it small.
# 2. keep an alphabetic order to avoid duplicates
RUN apt-get update \
 && mkdir -p /usr/share/man/man1 \
 && mkdir -p /usr/share/man/man7 \
 && apt-get install -y --no-install-recommends \
      bash \
      curl \
      htop \
      less \
      postgresql-client \
      tmux \
      vim

# Run as non root user (best practice)
WORKDIR /srv
COPY . .

# Run as a non-root user.
RUN useradd -ms $SHELL syapse \
 && chown -R syapse:syapse /home/syapse
USER syapse


# Install or update system dependencies
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIPENV_COLORBLIND=true \
    PIPENV_NOSPIN=true \
    PIP_NO_CACHE_DIR=off \
    PIP_USER=1 \
    PATH=$PATH:/home/syapse/.local/bin

RUN python -m pip install --upgrade --user pipenv

# Install project dependencies
RUN pipenv install --dev

# Set environment variables
# ENV MYVAR="Your_needed_env_variables"

# Set the command executed first when the container run
ENTRYPOINT ["./docker-entrypoint.sh"]

# Create a dev image for local development environments
FROM prod as dev

# Install environment dependencies with Pipenv.
RUN pipenv install --system --dev --skip-lock

# Mount a volume at /srv so code can be changed on the fly
VOLUME /srv
