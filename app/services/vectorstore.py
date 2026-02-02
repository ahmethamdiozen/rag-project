from app.core.config import collection

def save_to_chroma(
        texts: list[str], 
        embeddings: list[list[float]], 
        metadatas: list[dict]
    ):

    ids = [
        f"{meta['file_hash']}_{idx}"
        for idx, meta in enumerate(metadatas)
    ]

    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

def query_chroma(query_embedding: list[float], n_results: int = 5):
    
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )