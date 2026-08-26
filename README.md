# Offline AI Assistant

An offline AI-powered document assistant that allows users to upload PDF documents and ask context-aware questions using a locally hosted Large Language Model (Qwen3:4B) through Ollama.

The project uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded documents before generating an answer. It is designed to run locally without relying on cloud-based AI APIs.

## Tech Stack

- Python
- FastAPI
- Ollama
- Qwen3:4B
- PyMuPDF (fitz)
- Pydantic
- Embeddings
- Vector Similarity Search

## Features Completed

- Local LLM integration using Ollama and Qwen3:4B
- FastAPI backend with health check endpoints
- PDF upload API using FastAPI `UploadFile`
- PDF text extraction using PyMuPDF
- Text chunking for document processing
- Embedding generation for document chunks
- Local embedding storage
- Similarity-based retrieval of relevant document chunks
- RAG pipeline integration with Qwen3:4B
- Modular project structure for scalability

## Project Progress

### Day 1 — Ollama & Project Setup

- Created project structure and Python virtual environment.
- Installed and configured Ollama.
- Downloaded and tested the Qwen3:4B model locally.
- Built the first Python application using `ollama.chat()`.

### Day 2 — FastAPI Backend

- Integrated FastAPI backend.
- Added `GET /` and `GET /health` endpoints.
- Implemented `POST /upload` endpoint for PDF uploads.
- Built `document_loader.py` using PyMuPDF (`fitz`) to extract text from PDF documents.
- Connected uploaded PDFs with the text extraction pipeline.

### Day 3 — PDF Processing

- Tested the FastAPI application using Uvicorn and Swagger UI.
- Verified API endpoints for application health and document handling.
- Implemented PDF upload functionality using FastAPI `UploadFile`.
- Successfully processed uploaded PDF documents using PyMuPDF.
- Extracted textual content from PDF pages and stored the processed documents for further AI processing.

### Day 4 — Document Question Answering

- Implemented the `POST /ask` endpoint using FastAPI and Pydantic request models.
- Integrated Ollama's `chat()` API with the locally hosted Qwen3:4B model.
- Built prompt generation using processed document content and user questions.
- Tested end-to-end document question answering through FastAPI Swagger UI.

### Day 5 — RAG Embedding & Retrieval Pipeline

- Implemented document text chunking.
- Implemented embedding generation for document chunks.
- Added local embedding storage using JSON.
- Implemented similarity-based document retrieval.
- Added `retrieve_chunks()` functionality to retrieve the most relevant chunks for a user question.
- Integrated retrieved document context into the `/ask` endpoint.
- Tested the RAG retrieval pipeline using multiple documents.
- Verified embedding generation and vector similarity retrieval.

## RAG Pipeline

The current architecture follows this flow:

PDF Document  
↓  
Text Extraction  
↓  
Text Chunking  
↓  
Embedding Generation  
↓  
Vector Storage  
↓  
Similarity Search  
↓  
Relevant Chunks  
↓  
Qwen3:4B  
↓  
Final Answer

## Project Structure

```text
Offline-AI-Assistant/
│
├── app/
│   ├── main.py
│   └── schemas.py
│
├── data/
│   ├── processed/
│   ├── sample_documents/
│   └── uploads/
│
├── src/
│   ├── chunking.py
│   ├── document_loader.py
│   ├── embedding_service.py
│   ├── ocr_service.py
│   ├── retriever.py
│   └── vector_store.py
│
├── test_ch.py
├── test_rag_embedd.py
├── tst_emb.py
├── tst_retriever.py
├── tst_vector.py
│
├── app.py
├── requirements.txt
└── README.md
