import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")

MODEL_1 = os.getenv("HF_MODEL_1")
MODEL_2 = os.getenv("HF_MODEL_2")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}


def call_model(model, prompt):
    try:
        url = f"https://api-inference.huggingface.co/models/{model}"

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 300
            }
        }

        response = requests.post(url, headers=HEADERS, json=payload, timeout=20)

        result = response.json()

        if isinstance(result, list):
            return result[0]["generated_text"]

        if "error" in result:
            return None

        return None

    except Exception:
        return None


def generate_answer(query, docs):
    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are an expert automotive engineer.

Answer ONLY from the context below.

Context:
{context}

Question:
{query}

Answer:
"""

    # 🔹 Try Model 1
    answer = call_model(MODEL_1, prompt)

    if answer:
        return f"[Model: {MODEL_1}]\n{answer}"

    # 🔹 Fallback Model 2
    answer = call_model(MODEL_2, prompt)

    if answer:
        return f"[Model: {MODEL_2}]\n{answer}"

    return "All models failed to generate response."