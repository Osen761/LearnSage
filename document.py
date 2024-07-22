import os
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import (
    PyMuPDFLoader, 
    TextLoader, 
    UnstructuredCSVLoader, 
    UnstructuredExcelLoader,
    UnstructuredMarkdownLoader, 
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader
)


class DocumentLoader:

    def __init__(self, file_path):
        self.file_path = file_path

    def load(self) -> list:
        docs = []
        file_name, file_extension_with_dot = os.path.splitext(self.file_path)
        file_extension = file_extension_with_dot.strip(".")
        pages = self._load_document(self.file_path, file_extension)
        for page in pages:
            if page.page_content:
                docs.append({
                    "raw_content": page.page_content,
                    "url": os.path.basename(page.metadata['source'])
                })

        if not docs:
            raise ValueError("🤷 Failed to load any documents!")

        return docs

    def _load_document(self, file_path: str, file_extension: str) -> list:
        ret_data = []
        try:
            loader_dict = {
                "pdf": PyMuPDFLoader(file_path),
                "txt": TextLoader(file_path),
                "doc": UnstructuredWordDocumentLoader(file_path),
                "docx": UnstructuredWordDocumentLoader(file_path),
                "pptx": UnstructuredPowerPointLoader(file_path),
                "csv": UnstructuredCSVLoader(file_path, mode="elements"),
                "xls": UnstructuredExcelLoader(file_path, mode="elements"),
                "xlsx": UnstructuredExcelLoader(file_path, mode="elements"),
                "md": UnstructuredMarkdownLoader(file_path)
            }

            loader = loader_dict.get(file_extension, None)
            if loader:
                ret_data = loader.load()

        except Exception as e:
            print(f"Failed to load document: {file_path}")
            print(e)

        return ret_data
    
    @staticmethod
    def split_into_chunks(content, chunk_size=1000, chunk_overlap=200):
        """Splits the text content into chunks."""
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return text_splitter.split_text(content)


# # Path to the document file
# file_path = "documents/2406.10970v1.pdf"

# # Create an instance of DocumentLoader
# loader = DocumentLoader(file_path)

# # Load the document
# documents = loader.load()

# # Print the loaded documents
# for doc in documents:
#     print("Raw Content:", doc["raw_content"])
#     print("URL:", doc["url"])
