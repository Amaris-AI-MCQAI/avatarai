from .input_processor.process_inputs import ( 
    change_img_background,
)
from .avatar_constants import (
    FROM_INPUT,
)
from .Wav2Lip import inference
import uuid
import os
import subprocess
import shutil

dir_path = os.path.dirname(os.path.abspath(__file__))

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))

def create_avatar(form):
    # avatar = form['avatarFile']
    avatar = form['src_file']
    audio = form['audio_file']

    avatar_file_type = form['avatarFileType']
    background = form['background']

    unique_filename = uuid.uuid4().hex

    avatar_path = os.path.join(dir_path, 'Wav2Lip', 'temp', f'{unique_filename}_face.{avatar_file_type}')
    audio_path = os.path.join(dir_path, 'Wav2Lip', 'temp', f'{unique_filename}_audio.wav')

    temp_dir = os.path.join(dir_path, 'Wav2Lip', 'temp')
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)

    for path, item in {
        avatar_path : avatar, 
        audio_path : audio
    }.items():
        with open(path, "wb") as buffer:
            # Save avatar file
            shutil.copyfileobj(item.file, buffer)

    # Change background
    if avatar_file_type != 'mp4' and background != FROM_INPUT :
        print("Changing background")
        avatar_path = change_img_background(avatar_path, background)

    # Create avatar
    try:
        result_path = sync_with_text(audio_path=audio_path, face_path=avatar_path)
    except Exception as e:
        print("Error:")
        print(e)
        return("Error")

    return [result_path, avatar_path, audio_path]

def sync_with_text(audio_path, face_path):
    temp_folder_path = os.path.join(dir_path, "Wav2Lip", "temp")
    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
    file_name = face_path.split('.')[0]
    outfile_path = os.path.join(dir_path, "Wav2Lip", "temp", f"{file_name}_result.mp4")
    avi_path = os.path.join(dir_path, "Wav2Lip", "temp", "result.avi") 

    # text_to_wav(voice, transcript_text, audio_path)
    inference.generate(audio_path=audio_path, face_path=face_path, outfile_path=outfile_path)
    
    # Delete temp file
    remove_files([avi_path])

    return outfile_path

def remove_files(paths):
    for path in paths:
        if os.path.exists(path):
            os.remove(path)