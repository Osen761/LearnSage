import os
import logging
from mimetypes import guess_type
from dotenv import load_dotenv
import google.generativeai as genai
from document import DocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import PIL.Image as PIL

# Load environment variables
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")
os.environ["GOOGLE_API_KEY"] = api_key

# Generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create a client
client = genai.GenerativeModel(model_name="gemini-1.5-pro", generation_config=generation_config)

def upload_to_gemini(path, mime_type=None):
    """
    Uploads the given file to Gemini.
    """
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def split_into_chunks(content, chunk_size=1000, chunk_overlap=200):
    """
    Splits the text content into chunks using LangChain.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_text(content)


def process_videos(video_paths):
    """
    Processes multiple video files by uploading them to Gemini.
    """
    uploaded_files = []
    for video_path in video_paths:
        mime_type, _ = guess_type(video_path)
        if not mime_type:
            logging.error(f"Could not determine the MIME type of {video_path}")
            continue
        uploaded_files.append(upload_to_gemini(video_path, mime_type=mime_type))
    return uploaded_files

def process_documents(document_paths):
    """
    Processes multiple documents by loading and splitting their content.
    """
    all_document_content = ""
    for document_path in document_paths:
        loader = DocumentLoader(document_path)
        documents = loader.load()
        for doc in documents:
            all_document_content += doc['raw_content'] + "\n\n"
    chunks = split_into_chunks(all_document_content)
    return chunks

from PIL import Image


def analyze_images(question, image_paths):
    """
    Analyzes multiple images and answers a question about them.
    """
    # Open all images using PIL
    uploaded_files = [Image.open(image_path) for image_path in image_paths]
    
    # Define the prompt
    prompt = f"You are an AI learning assistant called LearnSage. You are going to help learners analyze images and then answer any questions about the image: {question}\n\n"
    
    # Choose a Gemini model.
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    
    # Generate content using the model, prompt, and uploaded files
    response = model.generate_content([prompt] + uploaded_files, request_options={"timeout": 600})
    
    return response.text

def analyze_videos(question, video_paths):
    """
    Analyzes videos.
    """
    uploaded_files = process_videos(video_paths)
    prompt = f"You are an ai learing assistant called LearnSage. you are going to help learners analyse videos and answer any questions about the video{question}\n\n"
    response = client.generate_content([prompt,uploaded_files], request_options={"timeout": 600})
    return response.text

def analyze_documents(question, document_paths):
    """
    Analyzes documents.
    """
    document_chunks = process_documents(document_paths)
   # Select 3/4 of the chunks
    num_chunks = len(document_chunks)
    selected_chunks = document_chunks[:(3 * num_chunks) // 4]
    prompt = f"You are an ai learing assistant called LearnSage. you are going to help learners analyse and summarize documents and the answer any questions about the documents  .{question}\n\n" + "\n\n".join(selected_chunks)
    response = client.generate_content([prompt], request_options={"timeout": 600})
    return response.text

