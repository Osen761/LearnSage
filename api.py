import streamlit as st

import os

def write_api_keys_to_env(google_api_key, assemblyai_api_key, tivaly_api_key):
    with open('.env', 'w') as f:
        f.write(f"GOOGLE_API_KEY={google_api_key}\n")
        f.write(f"ASSEMBLYAI_API_KEY={assemblyai_api_key}\n")
        f.write(f"TIVALY_API_KEY={tivaly_api_key}\n")



from dotenv import load_dotenv

def collect_api_keys():
	# Load environment variables from .env file
	load_dotenv()

	# Accessing API keys from environment variables
	google_api_key = os.getenv("GOOGLE_API_KEY")
	assemblyai_api_key = os.getenv("ASSEMBLYAI_API_KEY")
	tivaly_api_key = os.getenv("TIVALY_API_KEY")

	# Storing the API keys in Streamlit's session state
	st.session_state['GOOGLE_API_KEY'] = google_api_key
	st.session_state['ASSEMBLYAI_API_KEY'] = assemblyai_api_key
	st.session_state['TIVALY_API_KEY'] = tivaly_api_key


import streamlit as st

# Assuming write_api_keys_to_env is defined as above

def ui_collect_and_write_api_keys():
	st.sidebar.title("Configuration")

	# Input fields for API keys
	google_api_key = st.sidebar.text_input("Google API Key", "", type="password")
	assemblyai_api_key = st.sidebar.text_input("AssemblyAI API Key", "", type="password")
	tivaly_api_key = st.sidebar.text_input("Tivaly API Key", "", type="password")

	# Submit button in the sidebar
	if st.sidebar.button("Submit"):
		# Write the API keys to the .env file
		write_api_keys_to_env(google_api_key, assemblyai_api_key, tivaly_api_key)
		# Optionally, notify the user that the keys have been saved
		st.sidebar.success("API keys saved successfully!")

# Example usage
ui_collect_and_write_api_keys()

     


# Example usage
# collect_api_keys()
# if 'GOOGLE_API_KEY' in st.session_state:
#     use_google_api(st.session_state['GOOGLE_API_KEY'])