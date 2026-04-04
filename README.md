<div style="display:flex; justify-content:flex-end; margin:8px 0;">
  <div style="display:inline-flex; align-items:center; gap:10px;
              border:1px solid #c8952a55; border-radius:10px;
              padding:7px 14px 7px 8px; background:#fff;">
    <div style="width:34px;height:34px;border-radius:7px;background:#0b1a35;
                display:flex;align-items:center;justify-content:center;
                font-size:12px;font-weight:700;color:#c8952a;
                border:1px solid #c8952a44;font-family:monospace;">TK</div>
    <div>
      <div style="font-size:13px;font-weight:600;color:#111;">Tikaram</div>
      <div style="font-size:11px;color:#888;font-family:monospace;">2024TM05053</div>
    </div>
    <div style="width:1px;height:26px;background:#ddd;"></div>
    <div style="font-size:11px;color:#555;line-height:1.5;">
      M.Tech <strong>AIML</strong> · Sem 3<br>
      BITS Pilani <strong>WILP</strong>
    </div>
  </div>
</div>


# bootcamp_assignment_01
## Multimodal RAG System with FastAPI

### Course: Multimodal Retrieval-Augmented Generation Bootcamp

## 6. Problem Statement

## 1. Domain Identification  
This project is based on the domain of **automotive engineering**, focusing on **engine design, diagnostics, and service engineering**. Engineers and technicians rely on workshop manuals (such as Hino engine manuals) to understand engine systems, perform troubleshooting, and carry out maintenance. These manuals include a combination of text, tables, and engineering diagrams.

---

## 2. Problem Description  
Extracting useful information from these manuals is difficult and time-consuming. The documents are large and contain detailed technical content such as torque specifications, fault codes, and subsystem explanations.

Engineers often need quick answers like:
- What is the torque value for a component?  
- What are the causes of a fault code?  
- How does a system like fuel injection work?  

Traditional keyword search is not effective because it does not understand the meaning of queries. It also cannot properly interpret tables or diagrams. As a result, users must manually search through multiple pages, which is inefficient and error-prone.

---

## 3. Why This Problem Is Unique  
Automotive manuals have domain-specific challenges:
- Use of specialised technical terms  
- Important data stored in structured tables  
- Engineering diagrams that explain system behavior  
- Information spread across different sections  

A complete answer often requires combining text, tables, and diagrams. This makes the problem more complex than a general document question-answering task.

---

## 4. Why RAG Is the Right Approach  
Retrieval-Augmented Generation (RAG) is suitable for this problem because it retrieves relevant information directly from documents at query time.

Key advantages:
- Provides answers based on actual documents  
- Reduces incorrect or hallucinated responses  
- Works with semantic search (understands meaning)  
- No need for retraining when adding new data  

A multimodal RAG system can also handle text, tables, and images together, allowing better and more complete answers compared to traditional methods.

---

## 5. Expected Outcomes  
The system will enable users to:
- Ask technical questions about engine systems  
- Retrieve values from tables like torque specifications  
- Understand information from diagrams  
- Get answers with proper source references  

This will reduce time spent on manual searching and improve accuracy in diagnostics and maintenance tasks. The goal is to make complex workshop manuals easy to use through a simple question-answer interface.

## Technology Choices

This system is designed with a focus on practical usability, cost efficiency, and ease of deployment, while still supporting multimodal capabilities required for automotive engineering documents.

---

## 7. Architecture Overview

The system follows a modular Multimodal RAG architecture with two primary pipelines: ingestion and query processing.

### Ingestion Pipeline

When a PDF document is uploaded, it is parsed into three types of content:

* Text  
* Tables  
* Images  

Each type is processed separately:

* Text is split into smaller chunks using recursive chunking  
* Tables are converted into structured textual representations  
* Images are passed through a vision-language model to generate descriptive summaries  

All processed content is converted into vector embeddings and stored in a vector database along with metadata such as page number and content type.

### Query Pipeline

When a user submits a query:

1. The query is converted into an embedding  
2. Relevant chunks are retrieved using similarity search  
3. Retrieved context is passed to the LLM  
4. The LLM generates a response grounded in the retrieved content  
5. The system returns the answer along with source references  

### Architecture Diagram
```mermaid
flowchart TD

    A[User Upload PDF] --> B[FastAPI /ingest]

    B --> C[PDF Parser - PyMuPDF]
    
    C --> D1[Text Extraction]
    C --> D2[Table Extraction]
    C --> D3[Image Extraction]

    D3 --> E[Vision Model - HF BLIP]
    E --> F[Image Summary]

    D1 --> G[Chunking]
    D2 --> G
    F --> G

    G --> H[Embedding Model - MiniLM]
    H --> I[Vector DB - ChromaDB]

    J[User Query] --> K[FastAPI /query]
    K --> L[Retriever - Top K Search]
    L --> I

    I --> L
    L --> M[Relevant Chunks]

    M --> N1[LLM 1 - Flan-T5]
    M --> N2[LLM 2 - BloomZ]

    N1 --> O[Answer Selection]
    N2 --> O

    O --> P[Final Answer + Sources]
```
## 8. Technology Choices

Document Parser — PyMuPDF

PyMuPDF was chosen because it provides direct and reliable extraction of text and images from PDF documents.

Embedding Model — Sentence Transformers (all-MiniLM-L6-v2)

A local embedding model provides efficient semantic search for technical content.

Vector Store — ChromaDB

ChromaDB is used for storing embeddings along with metadata like page number and content type.

LLM — Hugging Face Inference API (Multi-Model)

The system uses Hugging Face Inference API with two free models:

Primary Model: google/flan-t5-base
Secondary Model: bigscience/bloomz-560m

If the primary model fails, the system automatically falls back to the secondary model. This improves robustness and ensures reliable response generation.

Vision Model — Hugging Face BLIP

Salesforce/blip-image-captioning-base is used to generate summaries from images, enabling multimodal retrieval.

Framework — Lightweight Custom + LangChain Utilities

A modular pipeline ensures flexibility and maintainability.

API Layer — FastAPI

FastAPI provides fast API development with built-in documentation support.
## 9. Setup Instructions

### 1. Clone Repository


### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file using `.env.example`

HF_TOKEN=your_huggingface_token_here

HF_MODEL_1=google/flan-t5-base
HF_MODEL_2=bigscience/bloomz-560m

HF_VISION_MODEL=Salesforce/blip-image-captioning-base
```

---

### 5. Run the Server

```bash
uvicorn main:app --reload
```

---

### 6. Access API

* Swagger UI: http://localhost:8000/docs
* Health Check: http://localhost:8000/health

---

### 7. Ingest Document

```bash
curl -X POST "http://localhost:8000/ingest" \
-F "file=@sample_documents/hino_manual.pdf"
```

---

### 8. Query System

```bash
curl -X POST "http://localhost:8000/query" \
-H "Content-Type: application/json" \
-d '{"query": "Explain turbocharger working"}'
```

---

## 10. API Documentation

### GET /health

Returns system status including number of indexed documents and uptime.

Example Response:

```json
{
  "status": "running",
  "documents_indexed": 1,
  "total_chunks": 1200,
  "uptime": "10 minutes"
}
```

---

### POST /ingest

Uploads and processes a PDF document.

Example Response:

```json
{
  "message": "Document ingested successfully",
  "text_chunks": 800,
  "table_chunks": 150,
  "image_chunks": 50,
  "processing_time": "25 seconds"
}
```

---

### POST /query

Accepts a natural language query and returns an answer with sources.

Example Request:

```json
{
  "query": "What is the torque specification for cylinder head?"
}
```

Example Response:

```json
{
  "answer": "The torque specification is 120 Nm...",
  "sources": [
    {
      "file": "hino_manual.pdf",
      "page": 45,
      "type": "table"
    }
  ]
}
```

---

### GET /docs

Provides Swagger UI for testing all endpoints.

---

## 11. Screenshots

The following screenshots demonstrate the working system:

* Swagger UI showing API endpoints
* Successful document ingestion
* Query result for text-based retrieval
* Query result for table-based retrieval
* Query result for image-based retrieval
* Health endpoint response

All screenshots are stored in the `screenshots/` directory.

---

## 12. Limitations & Future Work

### Limitations

* Image understanding depends on the quality of generated summaries
* Table conversion may lose some structural relationships
* Performance may reduce with very large documents
* No authentication or user access control implemented

---

### Future Work

* Improve table parsing using structured extraction methods
* Add evaluation metrics such as RAGAS
* Implement caching for faster query response
* Support multiple document filtering
* Add authentication and rate limiting
* Deploy using Docker for scalability

##  Architecture Overview
```mermaid
flowchart TD

    A[User Upload PDF] --> B[FastAPI /ingest]

    B --> C[PDF Parser - PyMuPDF]
    
    C --> D1[Text Extraction]
    C --> D2[Table Extraction]
    C --> D3[Image Extraction]

    D3 --> E[Vision Model - HF BLIP]
    E --> F[Image Summary]

    D1 --> G[Chunking]
    D2 --> G
    F --> G

    G --> H[Embedding Model - MiniLM]
    H --> I[Vector DB - ChromaDB]

    J[User Query] --> K[FastAPI /query]
    K --> L[Retriever - Top K Search]
    L --> I

    I --> L
    L --> M[Relevant Chunks]

    M --> N1[LLM 1 - Flan-T5]
    M --> N2[LLM 2 - BloomZ]

    N1 --> O[Answer Selection]
    N2 --> O

    O --> P[Final Answer + Sources]
```
### Key Features

- Supports **true multimodal retrieval** (text, tables, images)  
- Uses **HuggingFace BLIP model** for image understanding  
- Implements **metadata-aware retrieval** (page, source, type)  
- Uses **multi-model LLM fallback (Flan-T5 + BloomZ)**  
- Provides **grounded answers with references**  
- Designed for **automotive engineering documents**
