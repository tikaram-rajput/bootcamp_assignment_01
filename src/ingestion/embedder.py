from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

PERSIST_DIR = "chroma_db"


def build_vectorstore(chunks):
    texts = []
    metadatas = []

    for chunk in chunks:
        texts.append(chunk["content"])
        metadatas.append({
            "page": chunk.get("page"),
            "type": chunk.get("type", "text"),
            "source": chunk.get("source")
        })

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=PERSIST_DIR
    )

    return vectorstore