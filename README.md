
**Offline AI Assistant**

An offline AI-powered document assistant that allows users to upload PDF documents and ask context-aware questions using a locally hosted Large Language Model (Qwen3:4B) through Ollama. The project is built with Python and FastAPI and runs completely offline without cloud APIs.

**Tech Stack**

Python
FastAPI
Ollama
Qwen3:4B LLM
PyMuPDF (fitz)
Pydantic

**Features Completed**

Local LLM integration using Ollama and Qwen3:4B.
FastAPI backend with health check endpoints.
PDF upload API using UploadFile.
PDF text extraction using PyMuPDF.
Modular project structure for scalability.

**Project Progress**

**Day 1**

Created project structure and Python virtual environment.
Installed and configured Ollama.
Downloaded and tested the Qwen3:4B model locally.
Built the first Python application using ollama.chat().

**Day 2**

Integrated FastAPI backend.
Added GET / and GET /health endpoints.
Implemented POST /upload endpoint for PDF uploads.
Built document_loader.py using PyMuPDF (fitz) to extract text from PDF documents.
Connected uploaded PDFs with the text extraction pipeline.

**Upcoming Features**

Question answering on uploaded PDFs.
Retrieval-Augmented Generation (RAG).
Embedding generation and vector search.
OCR support for scanned PDFs.
Multi-document support and chat history.

**Project Status**

Currently under active development.
