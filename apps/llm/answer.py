import requests
from django.conf import settings

GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"

# ✅ Use a VERIFIED Groq-supported model
MODEL = "llama-3.1-8b-instant"



def generate_answer(context: str, question: str) -> str:
    system_prompt = (
        "You are a business assistant.\n"
        "Answer ONLY using the provided context.\n"
        "If the answer is not present in the context, say:\n"
        "'I’m not sure about that. Please contact the store.'"
    )

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": (
                    f"Context:\n{context}\n\n"
                    f"Question:\n{question}"
                ),
            },
        ],
        "temperature": 0.2,
        "max_tokens": 300,   # 🔴 REQUIRED by Groq
        "top_p": 1,
        "stream": False,
    }

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        GROQ_CHAT_URL,
        headers=headers,
        json=payload,
        timeout=20,
    )

    # 🔍 Debug visibility
    if response.status_code != 200:
        raise Exception(
            f"Groq API error {response.status_code}: {response.text}"
        )

    return response.json()["choices"][0]["message"]["content"].strip()
