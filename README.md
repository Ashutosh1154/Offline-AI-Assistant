# Offline AI Assistant

An offline AI-powered document assistant that allows users to upload PDF documents and ask context-aware questions using a locally hosted Large Language Model, **Qwen3:4B**, through Ollama.

The project uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from uploaded documents before generating an answer. It is designed to run locally without relying on cloud-based AI APIs, keeping document processing and AI inference on the user's machine.

---

## Tech Stack

### Backend
- Python
- FastAPI
- Uvicorn
- Pydantic

### AI & RAG
- Ollama
- Qwen3:4B
- Retrieval-Augmented Generation (RAG)
- Embeddings
- Semantic Search

### Document Processing
- PyMuPDF (fitz)
- Tesseract OCR
- Sentence-Aware Text Chunking

### Vector Database
- ChromaDB

### Frontend
- HTML
- CSS
- JavaScript

---

## Features

- Fully local LLM integration using Ollama and Qwen3:4B
- PDF upload and processing through FastAPI
- PDF text extraction using PyMuPDF
- OCR support for scanned and image-based PDF pages
- Mixed PDF support with page-level OCR fallback
- Sentence-aware text chunking
- Automatic embedding generation
- Persistent vector storage using ChromaDB
- Semantic similarity-based document retrieval
- Retrieval-Augmented Generation pipeline
- Multi-document indexing and selection
- Document-specific semantic retrieval
- Query preprocessing for improved retrieval
- Structured API error handling
- PDF file validation
- Responsive web interface
- Drag-and-drop PDF upload
- Document-selection dropdown
- Upload and indexing status messages
- AI response loading indicator
- Multi-question chat history
- Separate user and AI chat bubbles
- Automatic chat scrolling
- Desktop, tablet, and mobile responsive design

---

# Project Progress

## Day 1 — Ollama & Project Setup

- Created the project structure and Python virtual environment.
- Installed and configured Ollama.
- Downloaded and tested the Qwen3:4B model locally.
- Built the first Python application using `ollama.chat()`.

---

## Day 2 — FastAPI Backend

- Integrated the FastAPI backend.
- Added `GET /` and `GET /health` endpoints.
- Implemented the `POST /upload` endpoint for PDF uploads.
- Built `document_loader.py` using PyMuPDF (`fitz`) to extract text from PDF documents.
- Connected uploaded PDFs with the text extraction pipeline.

---

## Day 3 — PDF Processing

- Tested the FastAPI application using Uvicorn and Swagger UI.
- Verified API endpoints for application health and document handling.
- Implemented PDF uploads using FastAPI `UploadFile`.
- Successfully processed uploaded PDF documents using PyMuPDF.
- Extracted textual content from PDF pages.
- Stored processed document text for further AI processing.

---

## Day 4 — Document Question Answering

- Implemented the `POST /ask` endpoint using FastAPI and Pydantic request models.
- Integrated Ollama's `chat()` API with the locally hosted Qwen3:4B model.
- Built prompt generation using processed document content and user questions.
- Tested end-to-end document question answering through FastAPI Swagger UI.

---

## Day 5 — RAG Embedding & Retrieval Pipeline

- Implemented document text chunking.
- Added embedding generation for document chunks.
- Implemented local vector storage during the initial RAG development stage.
- Implemented similarity-based document retrieval.
- Added retrieval functionality to find relevant chunks for a user question.
- Integrated retrieved document context into the `/ask` endpoint.
- Tested the RAG retrieval pipeline using multiple documents.
- Verified embedding generation and vector similarity retrieval.

---

## Day 6 — Retrieval Improvements, OCR & Multi-Document Support

- Improved text chunking by replacing fixed character-based splitting with sentence-aware chunking.
- Added overlapping sentence context to reduce information loss between chunks.
- Added query preprocessing for natural-language questions.
- Added query transformation to improve definition-based retrieval.
- Improved Qwen3:4B response handling for document question answering.
- Increased model generation limits to improve answer completeness.
- Automated embedding generation directly inside the `/upload` endpoint.
- Removed the need to manually run embedding-generation scripts after each upload.
- Added `GET /documents` to list indexed documents.
- Added multi-document support.
- Updated `/ask` to accept both `question` and `document_name`.
- Added validation to ensure the selected document exists before retrieval.
- Added FastAPI `HTTPException` based error handling.
- Added PDF file-type validation.
- Integrated Tesseract OCR with PyMuPDF.
- Added page-level OCR fallback for scanned and mixed PDFs.
- Added `ocr_used` and `ocr_pages` information to upload responses.
- Successfully tested OCR using image-based PDF content.
- Verified end-to-end RAG question answering using notes, resumes, and technical documents.
- Replaced the initial local vector-storage implementation with persistent ChromaDB storage.
- Added ChromaDB-based semantic retrieval.
- Added document-specific filtering during vector search.

---

## Day 7 — Frontend UI, Chat History & RAG Interface

- Built a complete web-based frontend using HTML, CSS, and JavaScript.
- Designed a responsive two-column interface.
- Added a document upload sidebar and AI question-answering workspace.
- Added drag-and-drop PDF upload functionality.
- Added manual PDF file selection.
- Connected the frontend with the FastAPI `/upload` endpoint.
- Added upload processing states during text extraction, embedding generation, and indexing.
- Added document indexing status messages.
- Displayed the number of generated chunks after indexing.
- Displayed OCR page-count information after processing.
- Connected the frontend with `GET /documents`.
- Added a document-selection dropdown.
- Added document refresh functionality.
- Connected the frontend with `POST /ask`.
- Added a question input interface.
- Added question submission using the `Ask AI` button.
- Added `Enter` to submit questions.
- Added `Shift + Enter` for multi-line questions.
- Added an AI loading indicator while Qwen3:4B generates a response.
- Improved the Qwen3 response flow for document question answering.
- Increased retrieval from the top 2 to the top 3 relevant document chunks.
- Fixed incomplete and truncated AI responses.
- Added multi-question chat history.
- Preserved previous questions and answers during the current session.
- Added separate user and AI assistant chat bubbles.
- Added automatic chat scrolling for new messages.
- Added a conversation placeholder before the first question.
- Improved frontend validation for empty questions and missing document selection.
- Improved upload error handling.
- Added responsive styling for desktop, tablet, and mobile screens.
- Improved styling for cards, buttons, upload controls, messages, and loading states.

---

# Current RAG Architecture

```text
PDF Upload
    ↓
PDF Validation
    ↓
Page-Level Text Extraction
    ↓
Is Readable Text Available?
   ↙                     ↘
 Yes                     No
  ↓                       ↓
PyMuPDF              Tesseract OCR
   ↘                     ↙
          Extracted Text
                ↓
     Sentence-Aware Chunking
                ↓
       Embedding Generation
                ↓
         ChromaDB Storage
                ↓
        Document Selection
                ↓
          User Question
                ↓
        Query Processing
                ↓
        Semantic Retrieval
                ↓
     Relevant Top-K Chunks
                ↓
           Qwen3:4B
                ↓
          Final Answer
                ↓
         Chat Interface
```

---

# Application Workflow

```text
Open Offline AI Assistant
        ↓
Upload PDF
        ↓
Validate PDF
        ↓
Extract Text / Run OCR
        ↓
Create Text Chunks
        ↓
Generate Embeddings
        ↓
Store Vectors in ChromaDB
        ↓
Load Document into Dropdown
        ↓
Select Document
        ↓
Enter Question
        ↓
Retrieve Relevant Chunks
        ↓
Build RAG Context
        ↓
Send Context + Question to Qwen3:4B
        ↓
Generate Local Answer
        ↓
Display Question and Answer in Chat
        ↓
Ask Additional Questions
```

---

# Project Structure

```text
Offline-AI-Assistant/
│
├── app/
│   ├── main.py
│   └── schemas.py
│
├── data/
│   ├── processed/
│   ├── uploads/
│   └── chroma_db/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── src/
│   ├── chunking.py
│   ├── document_loader.py
│   ├── embedding_service.py
│   ├── ocr_service.py
│   ├── chroma_store.py
│   └── chroma_retriever.py
│
├── requirements.txt
└── README.md
```

---

# API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Loads the Offline AI Assistant web interface |
| `GET` | `/health` | Checks backend and model status |
| `GET` | `/documents` | Lists indexed documents |
| `POST` | `/upload` | Uploads and indexes a PDF |
| `POST` | `/ask` | Answers a question using the selected PDF |

---

## Example `/health` Response

```json
{
  "status": "running",
  "model": "qwen3:4b"
}
```

---

## Example `/ask` Request

```json
{
  "question": "What is a varactor diode?",
  "document_name": "rmt5&6"
}
```

## Example `/ask` Response

```json
{
  "question": "What is a varactor diode?",
  "document": "rmt5&6",
  "retrieved_chunks": 3,
  "answer": "A varactor diode is a reverse-biased semiconductor diode whose junction capacitance varies with the applied voltage."
}
```

---

## Example `/upload` Response

```json
{
  "message": "File uploaded and indexed successfully",
  "filename": "document.pdf",
  "document_name": "document",
  "text_length": 2630,
  "chunks_created": 4,
  "chroma_chunks_stored": 4,
  "ocr_used": true,
  "ocr_pages": 1
}
```

---

# How It Works

### 1. PDF Upload

The user uploads a PDF using the frontend.

FastAPI validates the uploaded file and stores it locally.

### 2. Text Extraction

PyMuPDF extracts readable text from each PDF page.

If readable text is unavailable, Tesseract OCR is used as a page-level fallback.

### 3. Sentence-Aware Chunking

The extracted text is divided into smaller sentence-aware chunks.

Overlapping context helps preserve information between adjacent chunks.

### 4. Embedding Generation

Each chunk is converted into a vector embedding representing its semantic meaning.

### 5. ChromaDB Storage

Document chunks and their embeddings are stored persistently in ChromaDB.

### 6. Document Selection

Indexed documents are retrieved using the `/documents` endpoint and displayed in the frontend.

The user selects the document that should be queried.

### 7. Semantic Retrieval

The user's question is processed and compared against the embeddings stored for the selected document.

The most relevant chunks are retrieved from ChromaDB.

### 8. RAG Context Generation

The retrieved chunks are combined to form the document context supplied to the language model.

### 9. Local LLM Response

The context and user question are sent to Qwen3:4B running locally through Ollama.

The model is instructed to generate its response using only information retrieved from the selected document.

### 10. Chat Interface

The question and generated answer are displayed as chat messages.

Multiple questions and responses remain visible throughout the current browser session.

---

# Running the Project

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Offline-AI-Assistant
```

## 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Install and Configure Ollama

Install Ollama on your machine and make sure the Ollama service is running.

Pull Qwen3:4B:

```bash
ollama pull qwen3:4b
```

Verify the installed model:

```bash
ollama list
```

## 5. Install Tesseract OCR

On Ubuntu/WSL:

```bash
sudo apt update
sudo apt install tesseract-ocr
```

Verify the installation:

```bash
tesseract --version
```

## 6. Start the Application

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

# Privacy

The application is designed to operate locally.

Uploaded PDFs, extracted text, embeddings, vector database contents, retrieved context, and AI-generated responses remain on the user's machine.

No cloud-based AI API is required for document question answering.

---

# Key Learning Outcomes

This project demonstrates practical experience with:

- Large Language Models (LLMs)
- Generative AI
- Retrieval-Augmented Generation (RAG)
- Prompt Engineering
- Embeddings
- Semantic Search
- Vector Databases
- ChromaDB
- Local LLM Deployment
- Ollama
- FastAPI
- REST APIs
- Pydantic
- PDF Processing
- OCR
- Text Chunking
- Information Retrieval
- Frontend and Backend Integration
- HTML
- CSS
- JavaScript
- Responsive Web Design

---

# Project Status

**Under Active Development**

The core RAG pipeline and frontend interface are functional.

The application currently supports PDF upload, PyMuPDF text extraction, OCR fallback for scanned pages, sentence-aware chunking, embedding generation, persistent ChromaDB storage, semantic document retrieval, multi-document selection, local Qwen3:4B answer generation, and multi-question chat history through a responsive web interface.