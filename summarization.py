from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from markdown import markdown
import streamlit as st
import os

def summary(learning_style:str,text:str) -> str:
    load_dotenv()
    output_parser = StrOutputParser()

    # Updated template to include session_memory
    template = f"""you are an AI-based learning assistant called LearnSage. You are designed to help students learn better by providing personalized learning resources.
     summarize the given text in a very detailed manner. You can generate content tailored to this learning style {learning_style}.
     You can help students with a variety of subjects, such as math, science, history, and more. You can also provide tips and strategies to help students improve their study skills and achieve academic success.
     given text: {text}
       """

    prompt = ChatPromptTemplate.from_template(template=template)

    api_key = os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0,google_api_key=st.secrets["GOOGLE_API_KEY"])

    chain = (
            RunnablePassthrough()
            | prompt
            | model
            | output_parser
    )

    response = chain.invoke({"text": text, "learning_style": learning_style})

   

    return response
