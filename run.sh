source ~/Amaris_AI/avatarai/env/bin/activate
cd ~/Amaris_AI/avatarai/src/
#python app.py
uvicorn app:app --reload --port 16000 --host 0.0.0.0 