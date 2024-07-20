import streamlit as st
from web_exploler import search_and_generate_response
from report_call import generate_report
import asyncio
from uploaded_files import indexing, retriver
import os
from yt_audio import process_youtube_audio_and_answer_query
import tempfile
import shutil
from google_api import analyze_documents, analyze_images, analyze_videos
from General_qn_Chatbot import general_chatbot
from summarization import summary
from QandA import generate_and_answer, generate_questions

# Initialize session state for storing responses
if 'responses' not in st.session_state:
    st.session_state.responses = []

# Function to save responses to a text file
def save_responses(responses):
    with open('responses.txt', 'w') as f:
        for response in responses:
            f.write(f"{response[0]}: {response[1]}\n")
            f.write(f"Answer: {response[2]}\n\n")

# Call the function to save responses
save_responses(st.session_state.responses)

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
    st.session_state.responses = []
    st.sidebar.write("New learning session started. All previous data has been cleared.")
    st.experimental_rerun()  # Rerun the app to reset the state

if st.sidebar.button("Learning Style"):
    learning_style = st.sidebar.selectbox("Choose your learning style:", ["Auditory", "Read/Write", "Kinesthetic"])
    st.sidebar.write(f"You selected {learning_style} learning style.")
    
    # # Store the learning style in a config file
    # with open('.config', 'w') as f:
    #     f.write(f'LEARNING_STYLE="{learning_style}"')

# Quick Internet Search in Sidebar
st.sidebar.subheader("Quick Internet Search")
search_query = st.sidebar.text_input("Enter search query")
if st.sidebar.button("Search"):
    st.sidebar.write("Searching for:", search_query)
    results = search_and_generate_response(search_query)
    st.sidebar.write(results)


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
    "Ask Questions", "Generate Report", "Interact With your Files", "Summarize Documents", 
    "Interact with Images", "Interact With Videos", "Upload Files", "Summarize Documents", 
    "Interact with YouTube", "Download Summary", "Generate Q&A"])

if page == "Ask Questions":
    st.subheader("Ask Questions")
    question = st.text_input("Enter your question")
    if st.button("Ask"):
        st.write("Answering question:", question)
        if 'responses' not in st.session_state:
            st.session_state.responses = ""
        answer,updated_sesssion_memory = general_chatbot(question,learning_style,st.session_state.responses)
        st.session_state.responses = updated_sesssion_memory 
        st.session_state.responses.append(("Question", question, answer))
        st.write(answer)

elif page == "Generate Report":
    st.subheader("Generate a Report")
    report_topic = st.text_input("Enter the topic for the report")
    report_types = st.selectbox('select a report format', ["Research Report", "Resource_report", "Outline_report"])
    report_format = st.selectbox("Select report format", ["PDF"])
    if st.button("Generate Report"):
        st.write("Generating report for:", report_topic)
        st.write("Report format:", report_format)
        st.write("Report type:", report_types)
        # Call your report generation function here
        report = asyncio.run(generate_report(report_topic, report_format))
        st.success("Report generated successfully!")
        # Display the generated report
        st.write("Report content:")
        st.session_state.responses.append(("Report", report_topic, report))
        st.write(report)
        st.write("Download the report using the button below.")
        st.download_button(
            label="Download Report",
            data=report,
            file_name=f"{report_topic}.pdf",
            mime="application/pdf"
        )

elif page == "Upload Files":
    # Define the path to the "input" folder within "documents_index"
    documents_index_path = "input"
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
        indexer.index_documents(documents_index_path)
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
        st.write("Asking question about the uploaded files:",)
        st.write("Question:", question)
        retriver = retriver.DocumentSearchAssistant()
        answer, docs = retriver.retrieve_and_answer(question)
        st.session_state.responses.append(("File Interaction", question, answer))
        st.write("Answer:", answer)
        st.write("Documents used:", docs)

elif page == "Summarize Documents":
    st.subheader("Summarize Documents")
    document = st.sidebar.file_uploader("Upload the document you want to summarize")
    question = st.text_input("Enter your question for the document")

    if document:
        st.sidebar.write("Uploaded document:", document.name)
        st.session_state.document = document
        
        if st.sidebar.button("Summarize"):
            st.sidebar.write("Summarizing document...")
            summurizer = analyze_documents(question, document)
            st.session_state.responses.append(("Document Summarization", document.name, summurizer))
            st.write(summurizer)

            if st.sidebar.button("Download Summary"):
                st.download_button(
                    label="Download Summary",
                    data=summurizer,
                    file_name="summary.txt",
                    mime="text/plain"
                )

elif page == "Interact with Images":
    st.subheader("Interact with Images")
    uploaded_images = st.sidebar.file_uploader("Upload Images", type=['jpg', 'png'], accept_multiple_files=True)
    question = st.text_input("Enter your question")
    if st.button("Ask") and uploaded_images:
        temp_file_paths = []  # List to store paths of temporary files
        for uploaded_image in uploaded_images:
            # Create a temporary file for each uploaded image
            temp_file_path = tempfile.mktemp(suffix="." + uploaded_image.name.split('.')[-1])
            # Copy the uploaded file content to the temporary file
            with open(temp_file_path, "wb") as temp_file:
                shutil.copyfileobj(uploaded_image, temp_file)
            temp_file_paths.append(temp_file_path)
        
        st.write("Answering question:", question)
        # Pass the list of temporary file paths to the analyze_images function
        results = analyze_images(question, temp_file_paths)
        st.session_state.responses.append(("Image Interaction", question, results))
        st.write(results)

elif page == "Interact with Videos":
    uploaded_videos = st.sidebar.file_uploader("Upload Videos", type=['mp4'], accept_multiple_files=True)
    st.subheader("Interact with Videos")
    question = st.text_input("Enter your question")
    if st.button("Ask"):
        temp_file_paths = []  # List to store paths of temporary files
        for uploaded_video in uploaded_videos:
            # Create a temporary file for each uploaded video
            temp_file_path = tempfile.mktemp(suffix="." + uploaded_video.name.split('.')[-1])
            # Copy the uploaded file content to the temporary file
            with open(temp_file_path, "wb") as temp_file:
                shutil.copyfileobj(uploaded_video, temp_file)
            temp_file_paths.append(temp_file_path)
        st.write("Answering question:", question)
        # Pass the list of temporary file paths to the analyze_videos function
        results = analyze_videos(question, temp_file_paths)
        st.session_state.responses.append(("Video Interaction", question, results))
        st.write(results)

elif page == "Download Summary":
    st.subheader("Download Summary of the Learning Session")
    download_format = st.selectbox("Select download format", ["PDF", "Word", "Text"])
    if st.button("Download"):
        st.write("Downloading summary of the learning session in", download_format, "format")
        summary = summary(learning_style,st.session_state.responses)
        st.download_button(
            label="Download Summary",
            data=summary,
            file_name=f"summary.{download_format.lower()}",
            mime="application/pdf"
        )

elif page == "Generate Q&A":
    st.subheader("Generate Questions and Answers")
    question_type = st.selectbox("Select question type", ["Multiple Choice", "Short Answer", "True/False"])
    if st.sidebar.button("Generate"):
        st.write("Generating", question_type, "Questions and Answers based on the learning session")
        questions = generate_questions(st.session_state.responses, question_type)
        st.write("Questions:")
        st.write(questions)
        if st.button("Answer Questions"):
            qa_content = generate_and_answer(st.session_state.responses, question_type, question_type)
            st.write("Answers:")
            st.session_state.responses.append(("Q&A Generation", questions, qa_content))
            st.write(qa_content)

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
        answer = asyncio.run(process_youtube_audio_and_answer_query(st.session_state.youtube_url, question))
        st.session_state.responses.append(("YouTube Interaction", question, answer))
        st.write("Answer:", answer)
