import requests
from django.conf import settings


def summarize_report(data, month_label):
    prompt = f"""
You are a business analyst.

Create a WhatsApp-friendly monthly business summary for a store owner.

Rules:
- Use ₹ for currency
- Use bullet points
- Be concise (6–8 lines)
- Do NOT invent numbers

MONTH: {month_label}

DATA:
{data}
"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        },
        timeout=15,
    )

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
