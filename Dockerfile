FROM python:3.8.18-alpine

ENV PYTHONUNBUFFERED 1

ADD requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /src
