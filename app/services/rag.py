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


def is_answer_grounded(question: str, answer: str, context: str) -> bool:
    prompt = f"""
Question:
{question}

Context:
{context}

Answer:
{answer}

Is the answer fully supported by the context?
Respond with only YES or NO.
"""
    response = openai_client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{"role": "user", "content": prompt}],
        temperature=0   
    )

    verdict = response.choices[0].message.content.strip().upper()

    return verdict == "YES"


def build_context(chunks: list[dict]) -> str:
    context_parts = []

    for c in chunks:
        context_parts.append(
              f"{c['text']}"
        )

    return "\n\n".join(context_parts)