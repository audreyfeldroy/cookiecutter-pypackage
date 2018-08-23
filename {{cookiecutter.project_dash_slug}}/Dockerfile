FROM python:3.6

# install tox
RUN pip install tox

WORKDIR /code

# Copy the project locally 
COPY . .

CMD ["tox"]

