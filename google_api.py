import os
import google.generativeai as genai
from dotenv import load_dotenv
from mimetypes import guess_type
import logging
from document import DocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv()

# Set your API key from .env file and update the environment variable
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
else:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

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
    """Uploads the given file to Gemini.

    See https://ai.google.dev/gemini-api/docs/prompting_with_media
    """
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def split_into_chunks(content, chunk_size=1000, chunk_overlap=200):
    """Splits the text content into chunks using LangChain."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_text(content)

def analyze(question, image_path=None, video_path=None, document_path=None):
    """Analyzes an image, video, or document.

    Args:
        question: The question to be answered.
        image_path: Local path to the image file (optional).
        video_path: Local path to the video file (optional).
        document_path: Local path to the document file (optional).

    Returns:
        The model's response as text.
    """
    uploaded_files = []
    all_document_content = ""

    if image_path:
        mime_type, _ = guess_type(image_path)
        if not mime_type:
            logging.error(f"Could not determine the MIME type of {image_path}")
            return None
        image_file = upload_to_gemini(image_path, mime_type=mime_type)
        uploaded_files.append(image_file)

    if video_path:
        mime_type, _ = guess_type(video_path)
        if not mime_type:
            logging.error(f"Could not determine the MIME type of {video_path}")
            return None
        video_file = upload_to_gemini(video_path, mime_type=mime_type)
        uploaded_files.append(video_file)

    if document_path:
        loader = DocumentLoader(path=document_path)
        documents = loader.load()
        for doc in documents:
            all_document_content += doc['raw_content'] + "\n\n"
        chunks = split_into_chunks(all_document_content)

    # Select the first two chunks
    selected_chunks = chunks[:2]

    # Construct the prompt
    prompt = f"You are a learning assistant. {question}\n\n" + "\n\n".join(selected_chunks)

    # Generate response
    response = client.generate_content([prompt], request_options={"timeout": 600})
    return response.text

# Example usage
question = "Summarize the key points in the provided context below."
document_path = "/home/osen/Downloads/LearnSage/documents"  # Replace with actual path

analysis = analyze(question, document_path=document_path)
print(analysis)
