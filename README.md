# Avatar

This module holds the Wav2Lip AI model for the Avatar. It receives processed inputs from the backend through a FastAPI endpoint and responds with the produced avatar video. 

Python 3.6 is required to install the dependencies.

Set-up:

    python3.6 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    cd src && bash install_weights.sh

Start FastAPI server:

    cd src && python app.py
