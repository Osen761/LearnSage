import streamlit as st
import os
from tempfile import NamedTemporaryFile
from google_api import analyze_documents  # Ensure this is correctly imported

def run_document_analysis():
	st.title('Document Summarization')

	# Step 2: Streamlit UI Components
	question = st.text_input("Question", "What is the main idea of the document?")
	uploaded_files = st.file_uploader("Choose document(s)", accept_multiple_files=True)
	analyze_button = st.button('Summarize...')

	if analyze_button and uploaded_files:
		document_paths = []

		# Step 3: File Handling
		for uploaded_file in uploaded_files:
			with NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1], dir="documents") as tmp_file:
				tmp_file.write(uploaded_file.getvalue())
				document_paths.append(tmp_file.name)

		# Step 4: Analysis
		if document_paths:
			result = analyze_documents(question, document_paths)
			st.write(result)

		# Step 5: Cleanup (optional)
		for path in document_paths:
			os.remove(path)

