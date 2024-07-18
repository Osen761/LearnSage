import streamlit as st
from web_exploler import search_and_generate_response
from report_call import generate_report
import asyncio
from uploaded_files import indexing ,retriver
import os




# Add API key input at the top of the sidebar
st.sidebar.title("Configuration")
google_api_key = st.sidebar.text_input("Gemini API Key", "", type="password")
if st.sidebar.button("Submit"):
    with open('.env', 'w') as f:
        f.write(f'GOOGLE_API_KEY="{google_api_key}"')

# Add "Start New Learning Session" button
if st.sidebar.button("Start New Learning Session"):
    # Reset or clear session state
    st.session_state.clear()  # Clears all session state
    st.sidebar.write("New learning session started. All previous data has been cleared.")
    st.experimental_rerun()  # Rerun the app to reset the state

# Quick Internet Search in Sidebar
st.sidebar.subheader("Quick Internet Search")
search_query = st.sidebar.text_input("Enter search query")
if st.sidebar.button("Search"):
    st.sidebar.write("Searching for:", search_query)
    results = search_and_generate_response(search_query)
    st.sidebar.write(results)
    # Call your quick internet search function here, using st.session_state.api_ke


# Home Page
st.title('_:blue[LEARNSAGE]_ :sunglasses:')
st.write("""
    Welcome to the AI Learning Assistant. Navigate through the sidebar to use the features.
    - **Generate Report:** Create a detailed report on a topic of your choice.
    - **Upload Files:** Upload documents to interact with and analyze.
    - **Summarize Documents:** Get a summary of your documents.
    - **Ask Questions:** Ask any question and get instant answers.
    - **Quick Internet Search:** Perform quick searches on the web.
    - **Download Summary:** Download a summary of your learning session.
    - **Generate Q&A:** Create questions and answers based on your learning material.
""")

# Sidebar Navigation
page = st.sidebar.selectbox("Choose a feature", [
    "Home", "Generate Report", "Upload Files", "Summarize Documents", 
    "Ask Questions","Interact with YouTube", "Download Summary", "Generate Q&A"])

if page == "Home":
    st.subheader("Home")
    st.write("Select a feature from the sidebar.")

elif page == "Generate Report":
    st.subheader("Generate a Report")
    report_topic = st.text_input("Enter the topic for the report")
    report_types = st.selectbox('select a report format',["Research Report","Resource_report","Outline_report"])
    report_format = st.selectbox("Select report format", ["PDF"])
    if st.button("Generate Report"):
        st.write("Generating report for:", report_topic)
        st.write("Report format:", report_format)
        st.write("Report type:", report_types)
        # Call your report generation function here
        report = asyncio.run(generate_report(report_topic,report_format))
        st.success("Report generated successfully!")
        # Display the generated report
        st.write("Report content:")
        # Display the report content here
        st.write(report)

elif page == "Upload Files":
    # Define the path to the "input" folder within "documents_index"
    documents_index_path = os.path.join(os.path.expanduser("~"), "LearnSage", "input")
    # Ensure the "input" folder exists
    os.makedirs(documents_index_path, exist_ok=True)

    # File uploader for multiple files
    uploaded_files = st.sidebar.file_uploader("Upload Documents", type=['txt', 'pdf', 'docx'], accept_multiple_files=True)

    # Process each uploaded file
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Save each file to the "input" folder
            file_path = os.path.join(documents_index_path, uploaded_file.name)
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            st.sidebar.success(f"File '{uploaded_file.name}' uploaded successfully to input folder.")

    # Button to trigger indexing of documents
    if st.sidebar.button("Index Documents"):
        st.sidebar.text("Indexing in progress...")
        # Call your indexing function here, passing the path to the "input" folder
        indexer = indexing.DocumentIndexer()
        indexer = (documents_index_path)
        st.sidebar.text("Indexing completed.")

    # Function to list document titles in the "input" folder
    def list_document_titles(folder_path):
        return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Display the titles of documents in the "input" folder
    document_titles = list_document_titles(documents_index_path)
    for title in document_titles:
        st.sidebar.text(title)
            

    st.subheader("Interact with Uploaded Files")
    question = st.text_input("Enter your question for the uploaded file")
    if st.button("Ask Question"):
        st.write("Asking question about the upploaded files:",)
        st.write("Question:", question)
        retriver = retriver.DocumentSearchAssistant()
        answer, docs = retriver.retrieve_and_answer("what is chain of thought?")
        st.write("Answer:", answer)
        st.write("Documents used:", docs)
        # Call your question answering function here, using st.session_state.api_key and selected_file_data

elif page == "Summarize Documents":
    st.sidebar.subheader("Summarize Documents")
    document = st.sidebar.file_uploader("Upload the document you want to summarize")

    if document:
        st.sidebar.write("Uploaded document:", document.name)
        st.session_state.document = document
        if st.sidebar.button("Summarize"):
            st.session_state.summary = "This is a placeholder summary. Replace this with actual summary generation logic."
            # Call your document summarization function here, using st.session_state.api_key
            # Example: st.session_state.summary = summarize_document(document, st.session_state.api_key)

    if 'summary' in st.session_state:
        st.subheader("Document Summary")
        st.write(st.session_state.summary)
        if st.button("Download Summary"):
            st.download_button(
                label="Download Summary",
                data=st.session_state.summary,
                file_name="summary.txt",
                mime="text/plain"
            )


elif page == "Ask Questions":
    st.subheader("Ask General Questions")
    question = st.text_input("Enter your question")
    if st.button("Ask"):
        st.write("Answering question:", question)
        # Call your question answering function here
        # Display the answer in a chat-like format

elif page == "Download Summary":
    st.subheader("Download Summary of the Learning Session")
    download_format = st.selectbox("Select download format", ["PDF", "Word", "Text"])
    if st.button("Download"):
        st.write("Downloading summary of the learning session in", download_format, "format")
        # Call your download summary function here

elif page == "Generate Q&A":
    st.subheader("Generate Questions and Answers")
    question_type = st.selectbox("Select question type", ["Multiple Choice", "Short Answer", "True/False"])
    if st.button("Generate"):
        st.write("Generating", question_type, "questions and answers based on the learning session")
        # Call your Q&A generation function here

elif page == "Interact with YouTube":
    st.sidebar.subheader("Interact with YouTube")
    youtube_url = st.sidebar.text_input("Enter the URL of the YouTube video you want to interact with")

    if youtube_url:
        st.sidebar.write("YouTube URL uploaded:", youtube_url)
        st.session_state.youtube_url = youtube_url

    st.subheader("Interact with YouTube Video")
    question = st.text_input("Enter your question for the YouTube video")
    if st.button("Ask Question"):
        st.write("Asking question about the YouTube video:", st.session_state.youtube_url)
        st.write("Question:", question)
        # Call your question answering function here, using st.session_state.api_key and st.session_state.youtube_url

