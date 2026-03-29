from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_text(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = []

    for doc in documents:
        splits = splitter.split_text(doc["content"])

        for chunk in splits:
            chunks.append({
                "content": chunk,
                "page": doc["page"],
                "type": doc["type"]
            })

    return chunks