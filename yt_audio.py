import os
import asyncio
import yt_dlp
from dotenv import load_dotenv
import assemblyai as aai
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import streamlit as st
# Load environment variables
load_dotenv()
ASSEMBLYAI_API_KEY = os.environ["ASSEMBLYAI_API_KEY"] =st.secrets["ASSEMBLYAI_API_KEY"]

def transcribe_audio(file_path, api_key, max_retries=3):
    """Transcribe audio using AssemblyAI with retry logic."""
    aai.settings.api_key = api_key
    transcriber = aai.Transcriber()
    
    for attempt in range(max_retries):
        try:
            transcript = transcriber.transcribe(file_path)
            if transcript.status == aai.TranscriptStatus.error:
                raise Exception(transcript.error)
            return transcript.text
        except Exception as e:
            print(f"Error during transcription (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt == max_retries - 1:
                return None

async def download_and_convert_audio(video_url, output_dir, filename="%(id)s.%(ext)s"):
    """Download and convert YouTube video to audio using yt_dlp."""
    ydl_opts = {
        'format': 'm4a/bestaudio/best',  # The best audio version in m4a format
        'outtmpl': os.path.join(output_dir, filename),  # Output template with directory and filename
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }],
        'quiet': True,  # Suppress verbose output
    }

    try:
        os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Download video; ydl.download expects a list of URLs
            error_code = ydl.download([video_url])

        if error_code != 0:
            raise Exception(f"yt-dlp failed to download the audio with error code: {error_code}")

        # Assuming the output filename is based on the video ID and m4a extension
        # This part might need adjustment based on actual requirements
        video_id = ydl.extract_info(video_url, download=False)['id']
        mp3_file_path = os.path.join(output_dir, f"{video_id}.m4a")
        print(f"Audio downloaded and converted successfully to: {mp3_file_path}")
        return mp3_file_path
    except Exception as e:
        print(f"Error downloading and converting audio: {str(e)}")
        return None

def clean_up_files(*file_paths):
    """Delete specified files."""
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            else:
                print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {str(e)}")

async def process_youtube_audio_and_answer_query(youtube_url, query, output_dir="output"):
    """Process YouTube audio and answer a query based on the transcription."""
    audio_path = await download_and_convert_audio(youtube_url, output_dir)
    if not audio_path:
        print("Skipping audio processing due to download/conversion failure.")
        return None
    
    transcribed_text = transcribe_audio(audio_path, ASSEMBLYAI_API_KEY)
    if not isinstance(transcribed_text, str):
        print(f"Transcription failed: {transcribed_text}")
        clean_up_files(audio_path)
        return None

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
    text_chunks = text_splitter.split_text(transcribed_text)
    api_key = os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=api_key)
    vector_store = FAISS.from_texts(text_chunks, embeddings)
    
    def build_qa_chain(vector_store, query):
        """Build and run the QA chain."""
        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0,google_api_key=api_key),
            chain_type="stuff",
            retriever=vector_store.as_retriever(),
        )
        return qa_chain.run(query)

    answer = build_qa_chain(vector_store, query)
    
    clean_up_files(audio_path)
    return answer


