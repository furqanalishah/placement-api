FROM python:3.8

WORKDIR /app

ADD ./requirements.txt /app/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt

ADD . /app

# Install pre-requisites
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    python3-dev \
    python3-lxml

