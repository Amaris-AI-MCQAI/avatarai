#!/bin/sh
SERVER="kaiwen98"
IMAGE_NAME="moodle-mcqai"
cat ~/my_password.txt | sudo docker login --username kaiwen98 --password-stdin
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt
python -m nltk.downloader stopwords
docker build --target python -t $SERVER/$IMAGE_NAME:latest --no-cache .
docker push $SERVER/$IMAGE_NAME:latest
