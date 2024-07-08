import os
import time
from dotenv import load_dotenv  # Import dotenv

import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini."""
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

def wait_for_files_active(files):
  """Waits for the given files to be active."""
  print("Waiting for file processing...")
  for name in (file.name for file in files):
    file = genai.get_file(name)
    while file.state.name == "PROCESSING":
      print(".", end="", flush=True)
      time.sleep(10)
      file = genai.get_file(name)
    if file.state.name != "ACTIVE":
      raise Exception(f"File {file.name} failed to process")
  print("...all files ready")
  print()

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

files = [
  upload_to_gemini("Sherlock Jr. (1924) - 10 Min Clip", mime_type="video/mp4"),
]

wait_for_files_active(files)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        files[0],
      ],
    },
    {
      "role": "user",
      "parts": [
        "what is in this video \n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "This is a silent film from the early 1900s called \"The Sleuth\". It is a comedy, and a good example of the early days of film making. ",
      ],
    },
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)