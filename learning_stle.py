import streamlit as st
import requests
import configparser

def determine_learning_style(answers):
    """
    Analyzes user responses and determines their preferred learning style.
    """
    text_score = 0
    audio_score = 0

    # Section 1: Text Processing
    for question in ["1a", "2a", "3a"]:
        if answers.get(question) == "a":
            text_score += 1
    for question in ["1b", "2b", "3b"]:
        if answers.get(question) == "b":
            audio_score += 1

    # Section 2: Audio Processing
    for question in ["1b", "2b", "3b"]:
        if answers.get(question) == "b":
            text_score += 1
    for question in ["1a", "2a", "3a"]:
        if answers.get(question) == "a":
            audio_score += 1

    if text_score > audio_score:
        return "Text"
    elif audio_score > text_score:
        return "Audio"
    else:
        return "Balanced"

def main():
    st.title("Learning Style Questionnaire")
    st.write("Instructions: Please answer the following questions honestly. There are no right or wrong answers. "
             "Your responses will help tailor content to your preferred learning style.")

    # --- Section 1: Text Processing ---
    st.header("Section 1: Text Processing")
    answers = {}
    answers["1a"] = st.radio("1. Comprehension: I understand information best when I can:",
                              ("a) Read it myself.", "b) Hear someone explain it."))
    answers["1b"] = st.radio("2. After reading a passage, I often find myself:",
                              ("a) Summarizing the key points in writing.", "b) Talking to myself about what I just read."))
    answers["2a"] = st.radio("3. When studying, I prefer to:",
                              ("a) Highlight or underline important information in text.",
                               "b) Listen to recordings and take notes by ear."))
    answers["2b"] = st.radio("4. I find it easier to remember information if I can:",
                              ("a) Review written notes or textbooks.", "b) Replay audio recordings or retell information verbally."))
    answers["3a"] = st.radio("5. When learning new material, I prefer to:",
                              ("a) Read at my own pace and reread if needed.", "b) Listen to lectures or explanations at a set pace."))
    answers["3b"] = st.radio("6. I find it helpful to:",
                              ("a) Go back and review specific sections of text.", "b) Rewind or fast-forward audio recordings."))

    # --- Section 2: Audio Processing ---
    st.header("Section 2: Audio Processing")
    answers["1a"] = st.radio("1. In a classroom setting, I learn more effectively by:",
                              ("a) Following along with written notes or slides.", "b) Actively listening to the instructor's lecture."))
    answers["1b"] = st.radio("2. I find myself:",
                              ("a) Taking detailed written notes during lectures.", "b) Asking clarifying questions during lectures."))
    answers["2a"] = st.radio("3. When listening to instructions, I prefer to:",
                              ("a) Have a written copy of the instructions to refer to later.",
                               "b) Focus on listening carefully and asking questions for clarification."))
    answers["2b"] = st.radio("4. I tend to remember information better if it is:",
                              ("a) Presented in a clear and concise written format.",
                               "b) Explained verbally with examples or stories."))
    answers["3a"] = st.radio("5. When listening to audio explanations, I find it helpful to:",
                              ("a) Pause and take notes to keep up with the information.",
                               "b) Listen actively and ask questions for clarification later."))
    answers["3b"] = st.radio("6. I am more engaged with learning material that is:",
                              ("a) Presented in a visually appealing and well-organized way.",
                               "b) Delivered in a clear and engaging voice with appropriate pauses and emphasis."))

    # --- Submit Button ---
    if st.button("Get Learning Style"):
        learning_style = determine_learning_style(answers)
        st.success(f"Based on your responses, your preferred learning style is: **{learning_style}**")

        # --- Send data to FastAPI backend (Optional) ---
        if st.button("Save Learning Style"):
            try:
                api_url = "http://localhost:8000/save_learning_style/"  # Replace with your FastAPI URL
                response = requests.post(api_url, json={"learning_style": learning_style})
                response.raise_for_status() 
                st.success(response.json().get("message", "Learning style saved successfully!"))
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred while saving: {e}")

if __name__ == "__main__":
    main()