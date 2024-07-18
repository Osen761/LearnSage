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

    def __init__(self, path):
        self.path = path

    def load(self) -> list:
        docs = []
        for root, dirs, files in os.walk(self.path):
            for file in files:
                file_path = os.path.join(root, file)
                file_name, file_extension_with_dot = os.path.splitext(file_path)
                file_extension = file_extension_with_dot.strip(".")
                pages = self._load_document(file_path, file_extension)
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
            print(f"Failed to load document : {file_path}")
            print(e)

        return ret_data
    
    def split_into_chunks(content, chunk_size=1000, chunk_overlap=200):
        """Splits the text content into chunks using LangChain."""
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return text_splitter.split_text(content)

    

def main():
    loader = DocumentLoader(path="documents")  # Replace with your directory
    documents = loader.load()
    
    all_content = ""
    for doc in documents:
        all_content += doc['raw_content'] + "\n\n"  # Adding a newline as a separator

    print(all_content)  # This will print the concatenated content of all documents

if __name__ == "__main__":
    main()