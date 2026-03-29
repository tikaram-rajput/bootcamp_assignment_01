from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from config.config import EMBEDDING_MODEL, CHROMA_DB_PATH

def load_vectorstore():

    embeddings = SentenceTransformerEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    return Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings
    )
