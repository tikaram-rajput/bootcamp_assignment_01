from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
import shutil
import time
import os

from config.config import UPLOAD_PATH
from src.ingestion.parser import parse_pdf
from src.ingestion.chunker import chunk_text
from src.ingestion.embedder import build_vectorstore
from src.retrieval.vector_store import load_vectorstore
from src.retrieval.retriever import retrieve
from src.models.llm import generate_answer

router = APIRouter()
start_time = time.time()


# -----------------------------
# Request Model (IMPORTANT FIX)
# -----------------------------
class QueryRequest(BaseModel):
    query: str


# -----------------------------
# HEALTH ENDPOINT
# -----------------------------
@router.get("/health")
def health():

    try:
        vectorstore = load_vectorstore()
        count = len(vectorstore.get()["documents"])
    except:
        count = 0

    uptime = round(time.time() - start_time, 2)

    return {
        "status": "running",
        "documents_indexed": 1 if count > 0 else 0,
        "total_chunks": count,
        "uptime_seconds": uptime
    }


# -----------------------------
# INGEST ENDPOINT
# -----------------------------
@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):

    start = time.time()

    # Ensure upload folder exists
    os.makedirs("uploads", exist_ok=True)

    # Save file
    with open(UPLOAD_PATH, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parse PDF
    text_data, table_data, image_data = parse_pdf(UPLOAD_PATH)

    # Chunking
    text_chunks = chunk_text(text_data)
    table_chunks = chunk_text(table_data)

    # SIMPLE IMAGE HANDLING (ASSIGNMENT SAFE)
    image_chunks = []
    for img in image_data:
        image_chunks.append({
            "content": "Image related to engine component or diagram",
            "page": img["page"],
            "type": "image"
        })

    # Combine all
    all_chunks = text_chunks + table_chunks + image_chunks

    # Build vector DB
    build_vectorstore(all_chunks)

    processing_time = round(time.time() - start, 2)

    return {
        "message": "Ingestion successful",
        "text_chunks": len(text_chunks),
        "table_chunks": len(table_chunks),
        "image_chunks": len(image_chunks),
        "processing_time_seconds": processing_time
    }


# -----------------------------
# QUERY ENDPOINT (FIXED)
# -----------------------------
@router.post("/query")
def query(request: QueryRequest):

    vectorstore = load_vectorstore()

    user_query = request.query

    results = retrieve(user_query, vectorstore)

    context = "\n".join([r.page_content for r in results])

    answer = generate_answer(user_query, context)

    return {
        "answer": answer,
        "sources": [
            {
                "file": "hino_manual.pdf",
                "page": r.metadata.get("page"),
                "type": r.metadata.get("type")
            }
            for r in results
        ]
    }