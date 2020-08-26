FROM python:3.8.5-alpine
ENV PYTHONUNBUFFERED 1

RUN apk update && apk upgrade && \
    apk add postgresql-libs postgresql-dev build-base 

RUN mkdir /code
WORKDIR /code

RUN pip install pipenv
COPY . /code/
RUN pipenv install
RUN pipenv run alembic upgrade head
