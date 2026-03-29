from fastapi import APIRouter, UploadFile, File
import shutil
import time

from config.config import UPLOAD_PATH
from src.ingestion.parser import parse_pdf
from src.ingestion.chunker import chunk_text
from src.ingestion.embedder import build_vectorstore
from src.retrieval.vector_store import load_vectorstore
from src.retrieval.retriever import retrieve
from src.models.llm import generate_answer
from src.models.vision import summarize_image

router = APIRouter()
start_time = time.time()


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


@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):

    start = time.time()

    with open(UPLOAD_PATH, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text_data, table_data, image_data = parse_pdf(UPLOAD_PATH)

    text_chunks = chunk_text(text_data)
    table_chunks = chunk_text(table_data)

    image_chunks = []
    for img in image_data:
        summary = summarize_image(img["image"])

        image_chunks.append({
            "content": summary,
            "page": img["page"],
            "type": "image"
        })

    all_chunks = text_chunks + table_chunks + image_chunks

    build_vectorstore(all_chunks)

    processing_time = round(time.time() - start, 2)

    return {
        "message": "Ingestion successful",
        "text_chunks": len(text_chunks),
        "table_chunks": len(table_chunks),
        "image_chunks": len(image_chunks),
        "processing_time_seconds": processing_time
    }


@router.post("/query")
def query(request: dict):

    vectorstore = load_vectorstore()

    results = retrieve(request["query"], vectorstore)

    context = "\n".join([r.page_content for r in results])

    answer = generate_answer(request["query"], context)

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