import requests
from django.conf import settings

GROQ_EMBED_URL = "https://api.groq.com/openai/v1/embeddings"
MODEL = "text-embedding-3-small"


def embed_texts(texts: list[str]) -> list[list[float]]:
    response = requests.post(
        GROQ_EMBED_URL,
        headers={
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "input": texts,
        },
        timeout=20,
    )
    response.raise_for_status()
    return [item["embedding"] for item in response.json()["data"]]
