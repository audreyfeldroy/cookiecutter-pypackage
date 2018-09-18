FROM python:3-alpine3.7

ENV PATH=$PATH:/home/user/.local/bin \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_USER=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIPENV_COLORBLIND=true \
    PIPENV_NOSPIN=true \
    SHELL=/bin/sh

# Install system-level packages.
RUN apk add --no-cache --update \
    build-base \
    git \
    libffi-dev \
    linux-headers \
    pcre-dev \
    postgresql-client \
    postgresql-dev \
    python3-dev

# Set a working directory
WORKDIR /srv

# Copy everything in the working directory
COPY . .

# Install the newest pipenv
RUN pip install --upgrade pip pipenv

# Install environment dependencies with Pipenv
RUN pipenv install --system --dev

# Call the entry point
ENTRYPOINT ["./docker-entrypoint.sh"]
