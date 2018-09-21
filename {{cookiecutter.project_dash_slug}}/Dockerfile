# Base Image
FROM python:3.6.6-alpine3.7

# Best practice: if you build contains several layers you should order them
# from the less frequently changed to the more frequently changed (caching)

# Install tools required for the project
# Best practice:
# 1. do not install unnecessary packages, keep it small.
# 2. keep an alphabetic order to avoid duplicates
RUN apk add --no-cache --update \
    build-base \
    git \
    libffi-dev \
    linux-headers \
    pcre-dev \
    postgresql-client \
    python3-dev

# Run as non root user (best practice)
ENV USERNAME=syapse
ENV PROJECT_NAME={{cookiecutter.project_dash_slug}}
WORKDIR /home/$USERNAME/$PROJECT_NAME
COPY . .
RUN addgroup -g 303 -S $USERNAME \
    && adduser -u 303 -S -G $USERNAME -h /home/$USERNAME $USERNAME
RUN chown -R $USERNAME:$USERNAME /home/$USERNAME/$PROJECT_NAME
USER $USERNAME

# Install or update system dependencies
ENV PIP_NO_CACHE_DIR=off
ENV PATH=$PATH:/home/$USERNAME/.local/bin
RUN pip install --upgrade --user pip pipenv

# Install project dependencies
RUN pipenv install --dev

# Set environment variables
# ENV MYVAR="Your_needed_env_variables"

# Set the command executed first when the container run
ENTRYPOINT ["./docker-entrypoint.sh"]
