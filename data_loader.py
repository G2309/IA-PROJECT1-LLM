import json
import os
from bs4 import BeautifulSoup 
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

pinecone.init(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("INDEX_NAME")
index = pinecone.Index(index_name)

embedding_model = OpenAIEmbeddings()

def process_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        text = soup.get_text()
    return text

def process_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return json.dumps(data)  # Convertirlo a string si es necesario

def insert_data(file_path, file_type):
    if file_type == 'html':
        text = process_html(file_path)
    elif file_type == 'json':
        text = process_json(file_path)
    else:
        raise ValueError("Formato de archivo no soportado. Usa 'html' o 'json'.")

    embedding = embedding_model.embed_query(text)
    
    index.upsert(vectors=[(file_path, embedding)])
    print(f"Datos insertados desde {file_path} en Pinecone.")

insert_data("./data/html/*.html", "html")
insert_data("./data/json/*.json", "json")

