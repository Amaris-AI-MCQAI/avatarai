FROM python:3.8-slim AS python

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
        libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# python stuff
COPY ./requirements.txt ./

RUN pip install --upgrade pip setuptools wheel scikit-build \
    && pip install -r /api/requirements.txt \
    && rm -rf /root/.cache/pip
    
RUN python -m spacy download en_core_web_sm
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader stopwords

# copy project source
COPY ./src .
