from google.cloud import speech
from google.cloud import texttospeech
from google.cloud import translate_v2 as translate
from pixellib.tune_bg import alter_bg
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


def change_img_background(image_path, background):
    colors = {'White':(255,255,255), 'Black':(0,0,0), 'Green':(0,255,0), 'Red':(209,52,52) , 'Blue':(0,128,255)}
    color = colors[background]
    output = change_bg.color_bg(image_path, color, detect = "person")
    output = output[:,:,::-1]
    img = Image.fromarray(output)
    img.save(image_path)
    return image_path
