from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from config.config import EMBEDDING_MODEL, CHROMA_DB_PATH

def build_vectorstore(chunks):

    texts = [c["content"] for c in chunks]

    metadatas = [
        {
            "page": c["page"],
            "type": c["type"]
        }
        for c in chunks
    ]

    embeddings = SentenceTransformerEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    vectorstore = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=CHROMA_DB_PATH
    )

    return vectorstore