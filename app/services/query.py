from app.services.embedding import embed_query
from app.services.vectorstore import query_chroma
from app.services.rag import ask_llm, build_context
from app.core.config import collection

def answer_question(question: str, n_results: int = 5, file_names: list[str] | None = None) -> str:

    chunks = retrieve_chunks(question, n_results=n_results, file_names=file_names)

    if not chunks:
        return{
            "answer": "No relevant information found in the selected documents.",
            "sources": []
        }
    
    context = build_context(chunks)
    answer = ask_llm(question=question, context=context)

    sources = extract_sources(chunks)

    return {
        "answer": answer,
        "sources": sources
    }


def retrieve_chunks(query: str, n_results: int = 3, file_names: list[str] | None = None):
    query_embedding = embed_query(query)

    where = None

    if file_names:
        where = {
            "file_name": {
                "$in": file_names
            }
        }

    print("FILTER:", where)

    results = query_chroma(query_embedding=query_embedding, n_results=n_results, where=where)

    print("RAW RESULT:", results)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]



    chunks = []

    for doc, meta, dist in zip(documents, metadatas, distances):
        chunks.append({
            "text": doc,
            "file_name": meta["file_name"],
            "page": meta["page"],
            "distances": dist
        })

    return chunks

def extract_sources(chunks: list[dict]):
    seen = set()
    sources = []

    for c in chunks:
        key = (c["file_name"], c["page"])

        if key not in seen:
            seen.add(key)
            sources.append({
                "file_name": c["file_name"],
                "page": c["page"]
            })
    return sources