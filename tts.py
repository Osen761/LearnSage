from gtts import gTTS
import os
import playsound
from STT import transcribe_audio
import streamlit as st  # Import the transcribe_audio function

def text_to_speech(text, filename):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    playsound.playsound(filename)

# Assuming you have your API key and the file URL
api_key = os.environ["ASSEMBLYAI_API_KEY"] == st.secrets["ASSEMBLYAI_API_KEY"]
file_url = "https://github.com/AssemblyAI-Community/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"

# Call the transcribe_audio function and store the returned text
transcribed_text = transcribe_audio(file_url, api_key)

# Use the transcribed text for text-to-speech
filename = "output.mp3"
text_to_speech(transcribed_text, filename)

# Example: Writing the transcribed text to a file
with open('transcribed_text.txt', 'w') as file:
    file.write(transcribed_text)