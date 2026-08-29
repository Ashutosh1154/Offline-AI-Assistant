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

### Day 6 — Retrieval Improvements, OCR & Multi-Document Support

* Improved text chunking by moving from fixed character-based splitting to sentence-aware chunking.
* Added overlapping sentence context to reduce broken words and incomplete chunks.
* Improved semantic retrieval by adding query preprocessing for natural-language questions such as `What is AI?`.
* Added query transformation to improve definition-based retrieval results.
* Diagnosed and fixed Qwen3:4B reasoning-output behavior by separating thinking output from the final response using `think=True`.
* Increased model generation limits to allow Qwen3:4B to complete reasoning before returning the final answer.
* Automated embedding generation directly inside the `/upload` endpoint.
* Removed the need to manually run embedding-generation test scripts after each document upload.
* Added `GET /documents` endpoint to list all indexed documents.
* Added multi-document support by allowing users to select a specific document while sending a question to `/ask`.
* Updated the `/ask` request model to accept both `question` and `document_name`.
* Added validation to ensure the selected document exists before retrieval.
* Added FastAPI `HTTPException` based error handling for invalid file types, missing documents, failed retrieval, failed embeddings, and model errors.
* Added PDF validation so only `.pdf` files are accepted.
* Integrated Tesseract OCR with PyMuPDF for scanned and image-based PDF documents.
* Added page-level OCR fallback for mixed PDFs containing both selectable text and scanned pages.
* Added OCR status information including `ocr_used` and `ocr_pages` in the upload response.
* Successfully tested OCR using screenshot-based PDF content and verified document question answering using OCR-extracted text.
* Verified end-to-end RAG question answering across multiple uploaded PDFs including notes, resumes, and technical documents.

### Updated RAG Pipeline

The current architecture now follows this flow:

```text
PDF Upload
    ↓
File Validation
    ↓
Page-Level Text Extraction
    ↓
Normal Text Available?
   ↙                ↘
 Yes                 No
  ↓                   ↓
PyMuPDF           Tesseract OCR
   ↘                ↙
      Extracted Text
           ↓
 Sentence-Aware Chunking
           ↓
   Embedding Generation
           ↓
 Local Vector Storage
           ↓
 Document Selection
           ↓
    User Question
           ↓
   Query Improvement
           ↓
 Similarity Retrieval
           ↓
 Relevant Top-K Chunks
           ↓
       Qwen3:4B
           ↓
     Final Answer
```

### Additional Features Completed

* Sentence-aware document chunking
* Query preprocessing for improved retrieval
* Automatic document indexing after upload
* Multi-document selection
* Document listing API
* PDF file validation
* Structured API error handling
* OCR support for scanned PDFs
* Mixed-page OCR support
* OCR page-count tracking
* Qwen3 thinking/final-response separation
* Dynamic document-specific retrieval

### Updated API Endpoints

```text
GET  /
GET  /health
GET  /documents
POST /upload
POST /ask
```

Example `/ask` request:

```json
{
  "question": "What is a varactor diode?",
  "document_name": "rmt5&6"
}
```

Example `/upload` response:

```json
{
  "message": "File uploaded and processed successfully",
  "filename": "document.pdf",
  "text_length": 2630,
  "chunks_created": 4,
  "embedding_file": "data/embeddings/document.json",
  "ocr_used": true,
  "ocr_pages": 1
}
```

### Next Development Goals

* Replace JSON-based vector storage with ChromaDB.
* Use persistent ChromaDB collections for document embeddings.
* Improve scalable vector similarity retrieval.
* Build a frontend using HTML, CSS, and JavaScript.
* Add PDF upload controls and document-selection dropdowns.
* Connect the frontend with `/upload`, `/documents`, and `/ask`.
* Add loading indicators, error messages, and response display.
* Clean temporary test scripts and finalize project structure.
* Update `requirements.txt` and final project documentation.

