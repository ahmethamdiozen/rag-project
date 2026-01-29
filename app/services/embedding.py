from app.core.config import openai_client



def embed_texts(texts: list[str]) -> list[list[float]]:
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )

    return [item.embedding for item in response.data]


def embed_query(query: str) -> list[float]:
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    return response.data[0].embedding

