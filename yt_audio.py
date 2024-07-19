import os
import asyncio
from sys import stderr
from dotenv import load_dotenv
import assemblyai as aai
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def transcribe_audio(file_url, api_key):
    aai.settings.api_key = api_key
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_url)
    if transcript.status == aai.TranscriptStatus.error:
        return transcript.error
    else:
        return transcript.text

def write_transcription_to_file(transcription, output_file):
    try:
        with open(output_file, 'w') as f:
            f.write(transcription)
        print(f"Transcription written to {output_file}")
    except Exception as e:
        print(f"Error writing transcription to file: {str(e)}")

async def download_and_convert_audio(video_url, output_dir, filename="audio.mp3"):
    try:
        os.makedirs(output_dir, exist_ok=True)
        mp3_file_path = os.path.join(output_dir, filename)
        process = await asyncio.create_subprocess_exec(
            'yt-dlp', '-f', 'bestaudio', '--extract-audio', '--audio-format', 'mp3', '-o', mp3_file_path, video_url,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise Exception(f"yt-dlp failed to download the audio: {stderr.decode()}")
        print(f"Audio downloaded and converted successfully to: {mp3_file_path}")
        return mp3_file_path
    except Exception as e:
        print(f"Error downloading and converting audio: {str(e)}")
        return None

def split_text(text, chunk_size=1500, chunk_overlap=150):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_text(text)

def build_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    return FAISS.from_texts(text_chunks, embeddings)

def create_qa_chain(vector_store):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    return RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_store.as_retriever())

async def process_youtube_audio(youtube_url, query, output_dir="output"):
    load_dotenv()
    ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
    audio_path = await download_and_convert_audio(youtube_url, output_dir)
    if not audio_path:
        print("Skipping audio processing due to download/conversion failure.")
        return None
    transcribed_text = transcribe_audio(audio_path, ASSEMBLYAI_API_KEY)  # Call synchronously
    if not isinstance(transcribed_text, str):
        print(f"Transcription failed: {transcribed_text}")
        return None
    text_chunks = split_text(transcribed_text)
    vector_store = build_vector_store(text_chunks)
    qa_chain = create_qa_chain(vector_store)
    answer = qa_chain.run(query)
    return answer
