from langchain_community.document_loaders.blob_loaders.youtube_audio import (
    YoutubeAudioLoader,
)
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import (
    OpenAIWhisperParser,
    OpenAIWhisperParserLocal,
)
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_youtube_videos(urls, save_dir, local=True, query=""):
    """
    Process YouTube videos to transcribe, split, index, and run a QA chain.

    Args:
        urls (list): List of YouTube video URLs.
        save_dir (str): Directory to save audio files.
        local (bool): Flag to switch between local and remote parsing.
        query (str): The question to ask in the QA chain.

    Returns:
        str: The answer to the query.
    """
    # Transcribe the videos to text
    if local:
        loader = GenericLoader(
            YoutubeAudioLoader(urls, save_dir), OpenAIWhisperParserLocal()
        )
    else:
        loader = GenericLoader(YoutubeAudioLoader(urls, save_dir), OpenAIWhisperParser())
    docs = loader.load()
    
    # Combine doc
    combined_docs = [doc.page_content for doc in docs]
    text = " ".join(combined_docs)

    # Split them
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
    splits = text_splitter.split_text(text)

    # Build an index
    embeddings = GoogleGenerativeAIEmbeddings()
    vectordb = FAISS.from_texts(splits, embeddings)

    # Build a QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatGoogleGenerativeAI(model="gpt-3.5-turbo", temperature=0),
        chain_type="stuff",
        retriever=vectordb.as_retriever(),
    )
    
    # Ask a question!
    return qa_chain.run(query)

# Example usage
urls = ["https://youtu.be/kCc8FmEb1nY", "https://youtu.be/VMj-3S1tku0"]
save_dir = "output"
query = "Why do we need to zero out the gradient before backprop at each step?"
answer = process_youtube_videos(urls, save_dir, local=False, query=query)
print(answer)