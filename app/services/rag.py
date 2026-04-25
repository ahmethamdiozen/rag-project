import json
from typing import Generator
from app.core.config import openai_client

SYSTEM_PROMPT = (
    "You are a helpful assistant. "
    "Answer the question using ONLY the context below. "
    "If the answer is not in the context, say you don't know."
)

def ask_llm(question: str, context: str) -> str:
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"},
        ],
        temperature=0,
    )
    return response.choices[0].message.content


def stream_llm(question: str, context: str) -> Generator[str, None, None]:
    stream = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"},
        ],
        temperature=0,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield f"data: {json.dumps({'type': 'token', 'content': delta})}\n\n"


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