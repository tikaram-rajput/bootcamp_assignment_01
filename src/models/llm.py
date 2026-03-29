def generate_answer(query, context):

    prompt = f"""
    Answer the question based only on the context.

    Context:
    {context}

    Question:
    {query}
    """

    # Placeholder (will upgrade later)
    return "Answer generated based on retrieved context."
