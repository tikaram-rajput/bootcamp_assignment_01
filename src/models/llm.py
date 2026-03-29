import google.generativeai as genai
from config.config import LLM_API_KEY

genai.configure(api_key=LLM_API_KEY)

model = genai.GenerativeModel("gemini-pro")

def generate_answer(query, context):

    prompt = f"""
    You are an automotive engineering expert.

    Answer ONLY from the context below.
    If answer is not available, say:
    "Not available in document".

    Context:
    {context}

    Question:
    {query}
    """

    response = model.generate_content(prompt)

    return response.text