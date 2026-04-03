"""
╔══════════════════════════════════════════════════════════════════╗
║           MULTIMODAL RAG SYSTEM — BITS PILANI WILP               ║
╠══════════════════════════════════════════════════════════════════╣
║  Name        : Tikaram                                           ║
║  Roll No     : 2024TM05053                                       ║
║  Programme   : M.Tech (Work Integrated Learning Programme)       ║
║  Institute   : BITS Pilani                                       ║
║  Course      : Multimodal Retrieval-Augmented Generation         ║
║  Assignment  : Multimodal RAG System with FastAPI (Bootcamp-Sem3)║
╚══════════════════════════════════════════════════════════════════╝

System Overview:
    - POST /ingest  → Upload a PDF; extracts text, tables, images
    - POST /query   → Natural language Q&A over ingested documents
    - GET  /health  → System status and index statistics
    - GET  /docs    → Auto-generated Swagger/OpenAPI documentation
    - GET  /documents → Breakdown of indexed chunks by type
"""

from fastapi import FastAPI

from src.api.routes import router

app = FastAPI(
    title="Multimodal RAG System",
    description=(
        "**Author:** Tikaram &nbsp;|&nbsp; "
        "**Roll No:** 2024TM05053 &nbsp;|&nbsp; "
        "**Institute:** BITS Pilani WILP\n\n"
        "An end-to-end Multimodal RAG system that ingests PDF documents "
        "(text, tables, and images) and answers natural language queries "
        "with grounded answers and source references."
    ),
    version="1.0.0",
    contact={
        "name": "Tikaram",
        "url": "https://github.com/2024tm05053",
    },
    license_info={
        "name": "BITS Pilani WILP — Academic Assignment",
    },
)

from fastapi import FastAPI

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Multimodal RAG System")

app.include_router(router)


@app.get("/")
def home():
    return {"message": "RAG system running"}