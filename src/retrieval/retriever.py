def retrieve(query, vectorstore, k=3):
    return vectorstore.similarity_search(query, k=k)
