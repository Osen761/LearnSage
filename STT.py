import os
from dotenv import load_dotenv
import assemblyai as aai
import streamlit as st

def transcribe_audio(file_url, api_key):
    """
    Transcribes audio from a given file URL using AssemblyAI.

    Parameters:
    - file_url: URL of the audio file to transcribe.
    - api_key: AssemblyAI API key.

    Returns:
    - The transcribed text if successful, or an error message if not.
    """
    # Set the API key
    aai.settings.api_key = api_key

    # Initialize the transcriber
    transcriber = aai.Transcriber()
    
    # Perform transcription
    transcript = transcriber.transcribe(file_url)

    # Check the transcription status
    if transcript.status == aai.TranscriptStatus.error:
        return transcript.error
    else:
        return transcript.text

def write_transcription_to_file(transcription, output_file):
    """
    Writes the transcribed text to a file.

    Parameters:
    - transcription: The transcribed text.
    - output_file: The path to the output file.
    """
    try:
        with open(output_file, 'w') as f:
            f.write(transcription)
        print(f"Transcription written to {output_file}")
    except Exception as e:
        print(f"Error writing transcription to file: {str(e)}")

# Load environment variables
load_dotenv()

# Get the API key from .env file
ASSEMBLYAI_API_KEY = os.environ["ASSEMBLYAI_API_KEY"] = st.secrets["ASSEMBLYAI_API_KEY"]

# URL of the file to transcribe
FILE_URL = "/home/osen/Music/input/audio.mp3"

# Call the function to transcribe the audio
transcribed_text = transcribe_audio(FILE_URL, ASSEMBLYAI_API_KEY)

# Check if transcription was successful and write to file
if isinstance(transcribed_text, str):
    output_file = "/home/osen/Music/transcription.txt"
    write_transcription_to_file(transcribed_text, output_file)
else:
    print(f"Transcription failed: {transcribed_text}")
