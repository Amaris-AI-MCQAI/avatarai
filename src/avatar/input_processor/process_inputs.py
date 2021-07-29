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

def change_img_background(image_path, background):
    colors = {'White':(255,255,255), 'Black':(0,0,0), 'Green':(0,255,0), 'Red':(209,52,52) , 'Blue':(0,128,255)}
    color = colors[background]
    output = change_bg.color_bg(image_path, color, detect = "person")
    output = output[:,:,::-1]
    img = Image.fromarray(output)
    img.save(image_path)
    return image_path
