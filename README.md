# Avatar AI Model

This module contains the Wav2Lip AI model for the Avatar. It receives processed inputs from the backend through a FastAPI endpoint and responds with the produced avatar video. 

Python 3.6 is required to install the dependencies. After installing Python 3.6, run the following commands to set up and start the server.

Set Up:

    python3.6 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    cd src && bash install_weights.sh
    sudo apt install ffmpeg

Start FastAPI server:

    cd src && python app.py

## API Endpoint

The API methods are defined in src/app.py . There is one endpoint method *get_avatar_request*. The API endpoint will receive a form from the backend. The form received will be passed to the *create_avatar* method (see below) to do processing.

## Request Processing

The request form will be processed in src/avatar/create_avatar.py . The *create_avatar* method extracts the files (audio and image/video) and passes them to the inference method (see below) from the form. The background changing for images using the Pixellib module is also done in this method.

## Inference

The main AI model inference code is in src/avatar/Wav2Lip/inference.py . The model inputs are an audio file (the speech) and image/video file (avatar appearance). The code is mostly adapted from the Wav2Lip repository. For more details on Wav2Lip, visit the
[GitHub repository](https://github.com/Rudrabha/Wav2Lip).


## Pre-trained Weights

There are 4 pre-trained weights that will be downloaded when the install_weights.sh script is ran during set up:


| File                  | Directory Location                               | Used For    |
| -----------           | -----------                                      | ----------- |
| wav2lip_gan.pth       | src/avatar/Wav2Lip/checkpoints/                  | Wav2Lip lip-syncing  |
| wav2lip.pth           | src/avatar/Wav2Lip/checkpoints/                   | Wav2Lip lip-syncing  |          |
| s3fd.pth              | src/avatar/Wav2Lip/face_detection/detection/sfd/  | Face detection|
| xception_pascalvoc.pb | src/avatar/input_processor/                       | Pixellib background changer|

