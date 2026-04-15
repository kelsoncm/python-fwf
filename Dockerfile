FROM python:3.13.3-alpine

ENV PYTHONUNBUFFERED 1

ADD requirements-dev.txt /
RUN pip install -r /requirements-dev.txt

WORKDIR /src
