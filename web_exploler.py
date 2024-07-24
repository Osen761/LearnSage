from tavily import TavilyClient
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import streamlit as st

def search_and_generate_response(user_query):
    # Load environment variables
    load_dotenv()
    api_key = os.environ["TAVILY_API_KEY"] =st.secrets["TAVILY_API_KEY"]
 

    # Initialize TavilyClient and AI model
    tavily = TavilyClient(api_key=api_key)
    api_key = os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0,google_api_key=api_key)
    prompt_template = ChatPromptTemplate.from_template(template="""Answer the user’s question using the given context. In the context are documents that should contain an answer.make sure it is short and concise."
    'Documents:\n{context}\n\nQuestion: {query}'""")
    output_parser = StrOutputParser()

    if user_query:
        # Perform search
        response = tavily.search(query=user_query, search_depth="advanced")
        if 'results' in response:
            context = [{"url": obj["url"], "content": obj["content"]} for obj in response['results']]
            chain = (
                RunnablePassthrough()
                | prompt_template
                | model
                | output_parser
            )
            results = chain.invoke({"context": context, "query": user_query})
            return results
        else:
            return "Unexpected response structure: {}".format(response)
    else:
        return "Please enter a query to search."


