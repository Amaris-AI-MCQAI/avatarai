# mcqai

1. Download [Sense2Vec Pretrained Vectors](https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz).
2. Extract and move s2v_old folder into src/ai_model/s2v_old .

On shell:

    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    python -m nltk.downloader punkt
    python -m nltk.downloader stopwords
    python -m spacy download en_core_web_sm
    python app.py
