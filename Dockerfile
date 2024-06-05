FROM python:3.11.8-alpine

ENV PYTHONUNBUFFERED 1

ADD requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /src
