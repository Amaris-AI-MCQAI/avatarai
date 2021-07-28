from .input_processor.process_inputs import \
text_to_wav, speech_to_text, translate_text, change_background, extract_text
from .avatar_constants import (
    NO_TRANSLATION, TRANSCRIPT_FILE, TRANSCRIPT_TEXT,
    DOCX, PPTX, PDF, WAV,
    MIME_TO_EXT,
    FROM_IMAGE,
    NO_TRANSLATION
)
from .Wav2Lip import inference
import uuid
import os
import subprocess
import shutil

dir_path = os.path.dirname(os.path.abspath(__file__))

def create_avatar(form):
    avatar = form['avatarFile']
    avatar_file_type = form['avatarFileType']
    background = form['background']
    voice = form['voice']
    transcript_kind = form['transcriptKind']
    translate_to_language = form['translateToLanguage']

    unique_filename = uuid.uuid4().hex
    avatar_path = os.path.join(dir_path, 'Wav2Lip', 'temp', f'{unique_filename}.{avatar_file_type}')

    with open(avatar_path, "wb") as buffer:
        # Save avatar file
        shutil.copyfileobj(avatar.file, buffer)

    # Change background
    if background != FROM_IMAGE:
        print("Changing background")
        avatar_path = change_background(avatar_path, background)

    if transcript_kind == TRANSCRIPT_TEXT:
        transcript_text = form['transcriptText']
    elif transcript_kind == TRANSCRIPT_FILE:
        transcript_file = form['transcriptFile']
        transcript_file_type = form['transcriptFileType']
        transcript_path = os.path.join(dir_path, 'Wav2Lip', 'temp', 
        f'{unique_filename}.{MIME_TO_EXT[transcript_file_type]}')
        transcript_wav_path = os.path.join(dir_path, 'Wav2Lip', 'temp', 
        f'{unique_filename}.wav')        

        with open(transcript_path, "wb") as buffer:
            # Save transcript file
            shutil.copyfileobj(transcript_file.file, buffer)

        if transcript_file_type in [DOCX, PPTX, PDF]:
            print('Extracting text from document...')
            transcript_text = extract_text(transcript_path)
        elif transcript_file_type == WAV:
            transcript_orig_language = form['transcriptOrigLanguage']
            transcript_text = speech_to_text(transcript_path, transcript_orig_language)
        else:
            # If file is video
            print('Extracting raw audio...')
            transcript_orig_language = form['transcriptOrigLanguage']
            command = f'ffmpeg -y -i {transcript_path} -strict -2 {transcript_wav_path}'
            subprocess.call(command, shell=True)
            transcript_text = speech_to_text(transcript_wav_path, transcript_orig_language)
            
        remove_files([transcript_path, transcript_wav_path])

    # Translate language
    if translate_to_language != NO_TRANSLATION:
        print(f"Translating to {translate_to_language}...")
        transcript_text = translate_text(translate_to_language, transcript_text)

    # Create avatar
    try:
        result_path = sync_with_text(face_path=avatar_path, transcript_text=transcript_text, voice=voice)
        remove_files([avatar_path])
    except Exception as e:
        print("Error:")
        print(e)
        remove_files([avatar_path])
        return("Error")

    return result_path

def sync_with_text(face_path, transcript_text, voice):
    temp_folder_path = os.path.join(dir_path, "Wav2Lip", "temp")
    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)
    file_name = face_path.split('.')[0]
    audio_path = os.path.join(dir_path, "Wav2Lip", "temp", f"{file_name}.wav")
    outfile_path = os.path.join(dir_path, "Wav2Lip", "results", f"{file_name}.mp4")
    avi_path = os.path.join(dir_path, "Wav2Lip", "temp", "result.avi") 

    text_to_wav(voice, transcript_text, audio_path)
    inference.infer(audio_path=audio_path, face_path=face_path, outfile_path=outfile_path)
    
    # Delete temp files 
    temp_files = [audio_path, face_path, avi_path]
    remove_files(temp_files)

    return outfile_path

def remove_files(paths):
    for path in paths:
        if os.path.exists(path):
            os.remove(path)