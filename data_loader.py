import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.docstore.document import Document
from pinecone import Pinecone, ServerlessSpec

# Cargar variables de entorno
load_dotenv()

# Crear instancia de Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Crear el índice si no existe
if os.getenv("INDEX_NAME") not in pc.list_indexes().names():
    pc.create_index(
        name=os.getenv("INDEX_NAME"),
        dimension=1536,
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region=os.getenv("PINECONE_ENVIRONMENT")
        )
    )

# Inicializar embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

def ingest_docs() -> None:
    # Cargar documentos locales (puedes ajustar esto según tu necesidad)
    docs = [...]  # Aquí deberías agregar la lógica para cargar tus documentos locales.

    # Dividir los documentos en chunks para los embeddings
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    docs = text_splitter.split_documents(docs)

    print(f"Añadiendo {len(docs)} documentos a Pinecone.")

    # Subir los documentos al índice de Pinecone
    PineconeVectorStore.from_documents(
        docs, embeddings, index_name=os.getenv("INDEX_NAME")
    )

    print("Documentos locales cargados en Pinecone.")

