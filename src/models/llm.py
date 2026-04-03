import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def generate_answer(query, context):

    if not context:
        return "No relevant information found."

    prompt = f"""
You are an automotive engineering assistant.

Answer the question using ONLY the context below.

Context:
{context}

Question:
{query}
"""

    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating answer: {str(e)}"