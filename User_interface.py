import streamlit as st
from web_exploler import search_and_generate_response
from report_call import generate_report
import asyncio
from uploaded_files import indexing, retriver
import os
from yt_audio import process_youtube_audio_and_answer_query
from tempfile import NamedTemporaryFile
import tempfile
import shutil
from google_api import analyze_documents, analyze_images, analyze_videos
from General_qn_Chatbot import general_chatbot
from summarization import summary
from QandA import generate_and_answer, generate_questions

# Initialize session state for storing responses and learning style
if 'responses' not in st.session_state:
    st.session_state.responses = []
elif not isinstance(st.session_state.responses, list):
    st.session_state.responses = []
if 'learning_style' not in st.session_state:
    st.session_state.learning_style = ""

# Add API key input at the top of the sidebar
st.sidebar.title("Configuration")



# Input fields for API keys
google_api_key = st.sidebar.text_input("Google API Key", "", type="password")
assemblyai_api_key = st.sidebar.text_input("AssemblyAI API Key", "", type="password")
tivaly_api_key = st.sidebar.text_input("Tivaly API Key", "", type="password")

# Submit button in the sidebar
if st.sidebar.button("Submit"):
    # Storing the API keys in Streamlit's session state
    st.session_state['GOOGLE_API_KEY'] = google_api_key
    st.session_state['ASSEMBLYAI_API_KEY'] = assemblyai_api_key
    st.session_state['TIVALY_API_KEY'] = tivaly_api_key

# Example of accessing an API key from session state elsewhere in your application
# if 'GOOGLE_API_KEY' in st.session_state:
#     use_google_api(st.session_state['GOOGLE_API_KEY'])

# Add "Start New Learning Session" button
if st.sidebar.button("Start New Learning Session"):
    # Reset or clear session state
    st.session_state.clear()  
    st.session_state.responses = []
    st.session_state.learning_style = ""
    st.sidebar.write("New learning session started. All previous data has been cleared.")
    st.experimental_rerun()  # Rerun the app to reset the state

if st.sidebar.button("Learning Style"):
    learning_style = st.sidebar.selectbox("Choose your learning style:", ["Auditory", "Read/Write", "Kinesthetic"])
    st.session_state.learning_style = learning_style
    st.sidebar.write(f"You selected {learning_style} learning style.")

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
    "Ask Questions", "Generate Report", "Interact with your Files", "Summarize Documents", 
    "Interact with Images", "Interact With Videos", "Upload Files", "Summarize Documents", 
    "Interact with YouTube", "Download Summary", "Generate Q&A"])

if page == "Ask Questions":
    st.subheader("Ask Questions")
    question = st.text_input("Enter your question")
    if st.button("Ask"):
        st.write("Answering question:", question)
        if 'responses' not in st.session_state:
            st.session_state.responses = []
        answer= general_chatbot(question, st.session_state.learning_style)
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

elif page == "Interact with your Files":
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
        st.write("Asking question about the uploaded files:")
        st.write("Question:", question)
        retriever_instance = retriver.DocumentSearchAssistant()
        answer, docs = retriever_instance.retrieve_and_answer(question)
        st.session_state.responses.append(("File Interaction", question, answer))
        st.write("Answer:", answer)
        st.write("Documents used:", docs)

elif page == "Summarize Documents":
    
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
elif page == "Interact with Images":
    st.title('Image Analysis App')

    # Streamlit sidebar for inputs
    question = st.text_input('Question', 'What is in this image?')
    uploaded_files = st.sidebar.file_uploader("Choose images", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])

    if uploaded_files:
        image_paths = []
        for uploaded_file in uploaded_files:
            # Save the uploaded file to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                tmp.write(uploaded_file.getvalue())
                image_paths.append(tmp.name)
        
        if st.button('Analyze Images'):
            # Call the analyze_images function
            result = analyze_images(question, image_paths)
            
            # Display the resultt
            st.write(result)
            
            # Clean up: Remove temporary files
            for path in image_paths:
                os.remove(path)
    else:
        st.sidebar.write("Please upload at least one image.")

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
        # Unpack the list in st.session_state.responses to a string
        responses_str = ' '.join([' '.join(map(str, response)) for response in st.session_state.responses])
        session_summary = summary(st.session_state.learning_style, responses_str)
        st.write(session_summary)
        st.download_button(
            label="Download Summary",
            data=session_summary,
            file_name=f"summary.{download_format.lower()}",
            mime="application/pdf"
        )

elif page == "Generate Q&A":
    st.subheader("Generate Questions and Answers")
    question_type = st.selectbox("Select question type", ["Multiple Choice", "Short Answer", "True/False"])
    if st.sidebar.button("Generate"):
        responses_str = ' '.join([' '.join(map(str, response)) for response in st.session_state.responses])
        st.write("Generating", question_type, "Questions and Answers based on the learning session")
        
        # Generate questions
        questions = generate_questions(responses_str, question_type)
        st.write("Questions:")
        st.write(questions)
        
        # Store the generated questions for later use
        st.session_state.generated_questions = questions
        
        if st.button("Answer Questions"):
            # Ensure that generated_questions is available in the session state before proceeding
            if 'generated_questions' in st.session_state:
                # Use the stored questions as input for generating answers
                qa_content = generate_and_answer(st.session_state.generated_questions, question_type)
                st.write("Answers:")
                st.write(qa_content)
            else:
                st.write("Please generate questions first.")

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
