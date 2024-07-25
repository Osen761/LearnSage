import os
from dotenv import load_dotenv
import qdrant_client
from langchain_qdrant import Qdrant
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import streamlit as st

# Load environment variables
load_dotenv()

class DocumentSearchAssistant:
    def __init__(self, collection_name="MyCollection", model_name="models/embedding-001"):
        self.collection_name = collection_name
        self.model_name = model_name
        self.client = qdrant_client.QdrantClient(path="output")
        self.embedding_model = GoogleGenerativeAIEmbeddings(model=model_name)
        self.qdrant = Qdrant(self.client, collection_name, self.embedding_model)

    def search(self, query, k=10):
        found_docs = self.qdrant.similarity_search(query=query, k=k)
        return [{"id": i, "path": res.metadata.get("path"), "content": res.page_content} 
                for i, res in enumerate(found_docs)]

    def retrieve_and_answer(self, query,learning_style, k=10):
        found_docs = self.qdrant.similarity_search(query=query, k=k)
        
        context = ""
        mappings = {}
        for i, res in enumerate(found_docs):
            context += f"{i}\n{res.page_content}\n\n"
            mappings[i] = res.metadata.get("path")
        api_key = os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
        
        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0,google_api_key=api_key)
        prompt_template = (
            "Answer the user’s question using the documents given in the context. "
            "In the context are documents that should contain an answer. "
            "Please always reference the document ID (in square brackets, for example [0],[1]) of the document that was used to make a claim. "
            "Use as many citations and documents as it is necessary to answer a question.\n"
            "Documents:\n{context}\n\nQuestion: {query}"
            "generate content tailored to {learning_style} learners."
        )
        prompt = ChatPromptTemplate.from_template(template=prompt_template)
        chain = RunnablePassthrough() | prompt | model | StrOutputParser()
        
        result = chain.invoke({"context": context, "query": query})
        document_file_names = [os.path.basename(doc.metadata.get("path")) for doc in found_docs]
        return result, document_file_names


