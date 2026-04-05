from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import shutil
import os
import time

from src.ingestion.parser import parse_pdf
from src.ingestion.chunker import chunk_text
from src.ingestion.embedder import build_vectorstore
from src.ingestion.vision import summarize_image

from src.retrieval.retriever import get_retriever
from src.models.llm import generate_answer

router = APIRouter()

UPLOAD_PATH = "uploads"
os.makedirs(UPLOAD_PATH, exist_ok=True)


# -------------------- REQUEST MODEL --------------------
class QueryRequest(BaseModel):
    query: str


# -------------------- HEALTH --------------------
@router.get("/health")
def health():
    db_exists = os.path.exists("chroma_db")

    return {
        "status": "ok",
        "vector_db": "available" if db_exists else "not found",
        "models": "multi-LLM (HF API)",
        "uptime": "running"
    }


# -------------------- INGEST --------------------
@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    start = time.time()

    try:
        file_path = os.path.join(UPLOAD_PATH, file.filename)

        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # -------- PARSE PDF --------
        text, tables, images = parse_pdf(file_path)

        # -------- PROCESS IMAGES --------
        image_chunks = []
        for img in images:
            summary = summarize_image(img["image_bytes"])

            if not summary or "error" in summary.lower():
                summary = "Engineering diagram detected (details unavailable)"

            image_chunks.append({
                "content": summary,
                "page": img["page"],
                "type": "image",
                "source": file.filename
            })

        # -------- CHUNK TEXT & TABLE --------
        text_chunks = chunk_text(text)
        table_chunks = chunk_text(tables)

        for c in text_chunks:
            c["source"] = file.filename

        for c in table_chunks:
            c["source"] = file.filename

        all_chunks = text_chunks + table_chunks + image_chunks

        if len(all_chunks) == 0:
            raise HTTPException(status_code=400, detail="No content extracted from PDF")

        # -------- BUILD VECTOR STORE --------
        build_vectorstore(all_chunks)

        return {
            "message": "Ingestion successful",
            "text_chunks": len(text_chunks),
            "table_chunks": len(table_chunks),
            "image_chunks": len(image_chunks),
            "processing_time_seconds": round(time.time() - start, 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------- QUERY --------------------
@router.post("/query")
def query(request: QueryRequest):
    try:
        retriever = get_retriever()

        # ✅ NEW LANGCHAIN METHOD
        docs = retriever.invoke(request.query)

        print("DOCS FOUND:", len(docs))  # DEBUG

        if not docs:
            return {
                "question": request.query,
                "answer": "No relevant information found in documents.",
                "sources": []
            }

        # -------- GENERATE ANSWER --------
        answer = generate_answer(request.query, docs)

        # -------- FORMAT SOURCES --------
        sources = [{
            "content": d.page_content[:200],
            "page": d.metadata.get("page"),
            "type": d.metadata.get("type"),
            "source": d.metadata.get("source")
        } for d in docs]

        return {
            "question": request.query,
            "answer": answer,
            "sources": sources
        }

    except Exception as e:
        return {
            "question": request.query,
            "answer": f"System error: {str(e)}",
            "sources": []
        }