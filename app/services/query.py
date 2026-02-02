from app.services.embedding import embed_query
from app.services.vectorstore import query_chroma
from app.services.rag import ask_llm, build_context
from app.core.config import collection

def answer_question(question: str) -> str:

    chunks = retrieve_chunks(question)
    context = build_context(chunks)

    answer = ask_llm(question=question, context=context)

    sources = extract_sources(chunks)


    return {
        "answer": answer,
        "source": sources
    }


def retrieve_chunks(query: str, k: int = 3):
    query_embedding = embed_query(query)

    results = query_chroma(query_embedding=query_embedding, n_results=k)

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