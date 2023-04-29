FROM python:3.10-buster
LABEL author="Noah Gampe"
LABEL email="noah.gampe@gmail.com"

ARG DEPS="make"

WORKDIR /app
RUN apt-get update
RUN apt-get install -y --no-install-recommends $DEPS

ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

ADD . /app