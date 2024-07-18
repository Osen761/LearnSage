from langchain_community.vectorstores import FAISS
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
GOOGLE_EMBEDDING_MODEL = "models/embedding-001"

class Memory:
    def __init__(self, embedding_provider, **kwargs):
        if embedding_provider == "google":
            self._embeddings = GoogleGenerativeAIEmbeddings(model=GOOGLE_EMBEDDING_MODEL)
        else:
            raise Exception("Embedding provider not found.")

    def get_embeddings(self):
        return self._embeddings