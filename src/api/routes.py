from fastapi import APIRouter, UploadFile, File
import shutil

from config.config import UPLOAD_PATH
from src.ingestion.parser import parse_pdf
from src.ingestion.chunker import chunk_text
from src.ingestion.embedder import build_vectorstore
from src.retrieval.vector_store import load_vectorstore
from src.retrieval.retriever import retrieve
from src.models.llm import generate_answer

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "running"}


@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):

    with open(UPLOAD_PATH, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text_data, image_data = parse_pdf(UPLOAD_PATH)

    chunks = chunk_text(text_data)

    build_vectorstore(chunks)

    return {
        "message": "Ingestion successful",
        "text_chunks": len(chunks),
        "images_found": len(image_data)
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
                "page": r.metadata.get("page"),
                "type": r.metadata.get("type")
            }
            for r in results
        ]
    }
