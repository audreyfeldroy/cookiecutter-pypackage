FROM python:3.10-slim

WORKDIR /tmp

COPY src src
COPY requirements.txt requirements.txt
COPY pyproject.toml pyproject.toml
RUN pip install .
