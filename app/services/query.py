from app.services.embedding import embed_query
from app.services.vectorstore import query_chroma
from app.services.rag import ask_llm, build_context

def answer_question(question: str) -> str:
    query_embedding = embed_query(question)

    chroma_result = query_chroma(query_embedding=query_embedding, n_results=3)
    print(chroma_result)
    context = build_context(chroma_result=chroma_result)

    answer = ask_llm(question=question, context=context)

    return answer


