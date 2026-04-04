import requests
import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
URL = "https://openrouter.ai/api/v1/chat/completions"


def generate_answer(query, docs):
    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
You are an expert automotive engineer assistant.

Answer ONLY from the given context.
If answer not found, say "Not found in document".

Context:
{context}

Question:
{query}

Answer:
"""

    try:
        response = requests.post(
            URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "qwen/qwen3.6-plus:free",
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error generating answer: {str(e)}"