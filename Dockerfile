FROM python:3.6-slim AS python

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ Asia/Singapore

# set work directory
RUN mkdir /api
WORKDIR /api

# install dependencies
RUN set -eux \
    && apt-get update && apt-get install -y \
    	tzdata build-essential cmake \
        libffi-dev gcc musl-dev libxml2-dev libxslt-dev libjpeg-dev \
        libglib2.0-0 libsm6 libxext6 libxrender-dev ffmpeg\
    && rm -rf /var/lib/apt/lists/*

# python stuff
COPY ./requirements.txt ./

RUN pip install --upgrade pip setuptools wheel scikit-build \
    && pip install -r /api/requirements.txt \
    && rm -rf /root/.cache/pip
    
# copy project source
COPY ./src .

WORKDIR /api/src

# download sample data and weights
RUN ["chmod", "+x", "./download_weights.sh"]
RUN ./download_weights.sh