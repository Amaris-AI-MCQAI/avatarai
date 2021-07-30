#!/bin/sh
SERVER="kaiwen98"
IMAGE_NAME="moodle-avatarai"
cat ~/my_password.txt | sudo docker login --username kaiwen98 --password-stdin
docker build --target python -t $SERVER/$IMAGE_NAME:latest --no-cache .Dockerfile-GPU
docker push $SERVER/$IMAGE_NAME:latest
