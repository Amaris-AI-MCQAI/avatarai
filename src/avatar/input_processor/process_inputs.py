from google.cloud import speech
from google.cloud import texttospeech
from google.cloud import translate_v2 as translate
from pixellib.tune_bg import alter_bg
from text_extractor.extractor.DocumentExtractor import DocumentExtractor
from PIL import Image 
import os
import six
import io

dir_path = os.path.dirname(os.path.abspath(__file__))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(dir_path, 'api.json')

# Load model for background changer
change_bg = alter_bg(model_type = "pb")
change_bg.load_pascalvoc_model(os.path.join(dir_path, "xception_pascalvoc.pb"))
print('Pixellib Model Loaded')

# Convert text to speech
def text_to_wav(voice, text, output_path):
    
    language_code = "-".join(voice.split("-")[:2])
    text_input = texttospeech.SynthesisInput(text=text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    client = texttospeech.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )

    with open(output_path, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to "{output_path}"')
    return output_path

def speech_to_text(wav, language_code):
    # Instantiates a client
    client = speech.SpeechClient()
    with io.open(wav, "rb") as audio_file:
        content = audio_file.read()
    # The name of the audio file to transcribe
    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=language_code,
        enable_automatic_punctuation=True
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)
    transcript = ""

    for result in response.results:
        transcript = transcript + result.alternatives[0].transcript
        
    print("Transcript: {}".format(transcript))
    return transcript

def extract_text(doc_path):
    return DocumentExtractor().read_input(doc_path)

def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    print(u"Text: {}".format(result["input"]))
    print(u"Translation: {}".format(result["translatedText"]))
    print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
    return result["translatedText"]


def change_background(image_path, background):
    colors = {'White':(255,255,255), 'Black':(0,0,0), 'Green':(0,255,0), 'Red':(209,52,52) , 'Blue':(0,128,255)}
    color = colors[background]
    output = change_bg.color_bg(image_path, color, detect = "person")
    output = output[:,:,::-1]
    img = Image.fromarray(output)
    img.save(image_path)
    return image_path
