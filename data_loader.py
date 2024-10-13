import json
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.vectorstores import Pinecone
import pinecone

load_dotenv()

# Inicializar Pinecone y los embeddings
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("INDEX_NAME")
index = pinecone.Index(index_name)

embedding_model = OpenAIEmbeddings()

# Función para cargar y extraer texto de archivos HTML
def load_document_html(directory):
    documents = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".html"):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    soup = BeautifulSoup(file, 'html.parser')
                    text = soup.get_text(separator="\n")
                    document = Document(page_content=text, metadata={"source": filepath})
                    documents.append(document)
    return documents

# Función para cargar y extraer datos de archivos JSON
def load_document_json(directory):
    documents = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".json"):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    text = json.dumps(data)
                    document = Document(page_content=text, metadata={"source": filepath})
                    documents.append(document)
    return documents

# Función para dividir los documentos en chunks y subirlos a Pinecone
def ingest_docs(directory_html, directory_json):
    raw_documents_html = load_document_html(directory_html)
    raw_documents_json = load_document_json(directory_json)

    raw_documents = raw_documents_html + raw_documents_json

    print(f"Loaded {len(raw_documents)} documents")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    documents = text_splitter.split_documents(raw_documents)

    print(f"Split {len(documents)} documents into chunks")

    Pinecone.from_documents(
        documents, embedding=embedding_model, index_name=index_name
    )

    print(f"Inserted {len(documents)} chunks into Pinecone")

if __name__ == "__main__":
    directory_html = "./data/html"
    directory_json = "./data/json"
    ingest_docs(directory_html, directory_json)

