from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_text(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = []

    for doc in documents:
        split_docs = splitter.split_text(doc["content"])

        for chunk in split_docs:
            chunks.append({
                "content": chunk,
                "page": doc["page"],
                "type": doc["type"]
            })

    return chunks
