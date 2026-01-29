from app.core.config import openai_client

def ask_llm(question: str, context: str) -> str:
    prompt = f"""
You are a helpful assistant.
Answer the question using ONLY the context below.
If the answer is not in the context, say you don't know.

Context:
{context}

Question:
{question}
"""
     
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                    "role": "user", "content": prompt
            }
        ],
        temperature=0
    )


    print("CONTEXT:\n", context)

    return response.choices[0].message.content


def build_context(chroma_result) -> str:
    documents = chroma_result["documents"][0]

    return "\n\n".join(documents)

