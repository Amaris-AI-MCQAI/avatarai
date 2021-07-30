from .input_processor.process_inputs import ( 
    change_img_background,
)
from .avatar_constants import (
    FROM_INPUT,
)
from .Wav2Lip import inference
import uuid
import os
import shutil

dir_path = os.path.dirname(os.path.abspath(__file__))
temp_folder_path = os.path.join(dir_path, "Wav2Lip", "temp")

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))

def create_avatar(form):

    face = form['face_file']
    audio = form['audio_file']

    avatar_file_type = form['avatarFileType']
    background = form['background']

    unique_filename = uuid.uuid4().hex

    face_path = os.path.join(dir_path, 'Wav2Lip', 'temp', 
    f'{unique_filename}_face.{avatar_file_type}')
    audio_path = os.path.join(dir_path, 'Wav2Lip', 'temp', 
    f'{unique_filename}_audio.wav')

    if not os.path.exists(temp_folder_path):
        os.mkdir(temp_folder_path)

    for path, item in {
        face_path : face, 
        audio_path : audio
    }.items():
        # Save avatar file
        with open(path, "wb") as buffer:
            shutil.copyfileobj(item.file, buffer)

    # Change background
    if avatar_file_type != 'mp4' and background != FROM_INPUT :
        print("Changing background")
        face_path = change_img_background(face_path, background)

    # Create avatar
    try: 
        outfile_path = os.path.join(dir_path, "Wav2Lip", "temp", 
        f"{unique_filename}_result.mp4")
        avi_path = os.path.join(dir_path, "Wav2Lip", "temp", "result.avi") 
        inference.generate(audio_path=audio_path, 
        face_path=face_path, outfile_path=outfile_path)
    except Exception as e:
        remove_files([face_path, audio_path, avi_path])
        return({"Error": str(e)})


    return [outfile_path, avi_path, face_path, audio_path]


def remove_files(paths):
    for path in paths:
        if os.path.exists(path):
            os.remove(path)