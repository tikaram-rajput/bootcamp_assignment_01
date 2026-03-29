from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(title="Multimodal RAG System")

app.include_router(router)