import chromadb
from app.core.config import chroma_client

collection = chroma_client.get_or_create_collection(name="Docs")

def save_to_chroma(texts: list[str], embeddings: list[list[float]], metadatas: list[dict]):

    ids = [f"chunk_{i}" for i in range(len(texts))]

    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

def query_chroma(query_embedding: list[float], n_results: int = 5):
    
    return collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )