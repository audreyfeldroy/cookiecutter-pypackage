FROM python:3.9-slim

MAINTAINER {{ cookiecutter.full_name }} <{{ cookiecutter.email }}>

COPY . /tmp/project

RUN pip install /tmp/project && \
    rm -rf /tmp/project
