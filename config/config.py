import os
from dotenv import load_dotenv

load_dotenv()

# Paths
CHROMA_DB_PATH = "chroma_db"
UPLOAD_PATH = "sample_documents/temp.pdf"

# Chunking
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Models
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# API KEYS
LLM_API_KEY = os.getenv("LLM_API_KEY")
VISION_API_KEY = os.getenv("VISION_API_KEY")
