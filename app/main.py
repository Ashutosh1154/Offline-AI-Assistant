from fastapi import FastAPI, UploadFile, File, HTTPException
from app.schemas import QuestionRequest
import shutil
from pathlib import Path
from ollama import chat
from src.document_loader import save_text
from src.ocr_service import extract_text_with_ocr
from src.retriever import retrieve_chunks
from src.chunking import chunk_text
from src.embedding_service import generate_chunk_embeddings
from src.vector_store import save_embeddings


MODEL_NAME = "qwen3:4b"

app = FastAPI()


# Upload directory
UPLOAD_DIRECTORY = Path("data/uploads")
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)


# Embedding directory
EMBEDDING_DIRECTORY = Path("data/embeddings")
EMBEDDING_DIRECTORY.mkdir(parents=True, exist_ok=True)


@app.get("/")
def home():

    return {
        "message": "Welcome Ashutosh, FASTAPI is running"
    }


@app.get("/health")
def health():

    return {
        "status": "running",
        "model": MODEL_NAME
    }


@app.post("/upload")
def upload_document(file: UploadFile = File(...)):

    # Check if filename exists
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was provided."
        )

    # Allow only PDF files
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    # Create upload path
    file_path = UPLOAD_DIRECTORY / file.filename

    # Save uploaded PDF
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # Extract text normally using PyMuPDF
    try:
        document_text, ocr_pages = extract_text_with_ocr(
        file_path
    )

    except Exception as error:
        raise HTTPException(
        status_code=500,
        detail=f"Document extraction failed: {str(error)}"
    )

    used_ocr = ocr_pages > 0

    # If normal extraction produces almost no text,
    # try OCR instead
    if len(document_text.strip()) < 50:

        try:
            document_text = extract_text_with_ocr(
                file_path
            )

            used_ocr = True

        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"OCR failed: {str(error)}"
            )

    # Make sure some usable text exists
    if not document_text.strip():
        raise HTTPException(
            status_code=422,
            detail="No readable text could be extracted from the PDF."
        )

    # Save extracted text
    save_text(
        file_path.stem,
        document_text
    )

    # Create chunks
    chunks = chunk_text(
        document_text
    )

    if not chunks:
        raise HTTPException(
            status_code=422,
            detail="No text chunks could be created."
        )

    # Generate embeddings
    try:
        embedded_chunks = generate_chunk_embeddings(
            chunks
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Embedding generation failed: {str(error)}"
        )

    # Save embeddings
    embedding_file = save_embeddings(
        file_path.stem,
        embedded_chunks
    )

    return {
        "message": "File uploaded and processed successfully",
        "filename": file.filename,
        "text_length": len(document_text),
        "chunks_created": len(chunks),
        "embedding_file": str(embedding_file),
        "ocr_used": used_ocr,
        "ocr_pages": ocr_pages
    }


@app.get("/documents")
def list_documents():

    documents = [
        file.stem
        for file in EMBEDDING_DIRECTORY.glob("*.json")
    ]

    return {
        "documents": documents
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    # Check whether selected document exists
    embedding_file = (
        EMBEDDING_DIRECTORY
        / f"{request.document_name}.json"
    )

    if not embedding_file.exists():
        raise HTTPException(
            status_code=404,
            detail="Selected document was not found."
        )

    # Retrieve relevant chunks
    try:
        retrieved_chunks = retrieve_chunks(
            question=request.question,
            document_name=request.document_name,
            top_k=3
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Document retrieval failed: {str(error)}"
        )

    if not retrieved_chunks:
        raise HTTPException(
            status_code=404,
            detail="No relevant information found in the document."
        )

    # Combine retrieved chunks into context
    context = "\n\n".join(
        chunk["text"]
        for chunk in retrieved_chunks
    )

    # Create prompt for Qwen3
    prompt = f"""
Answer the QUESTION using only the CONTEXT.

Return ONLY the final answer.
Do not explain your reasoning.
Do not describe what you are doing.
Do not say "the user asked", "the context says", or similar phrases.
Do not repeat the question.
Keep the answer concise.

If the answer is not present in the CONTEXT, return exactly:
The answer is not available in the uploaded document.

CONTEXT:
{context}

QUESTION:
{request.question}

FINAL ANSWER ONLY:
"""

    # Send context and question to Qwen3
    try:
        response = chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            think=True,
            options={
                "num_predict": 2000,
                "temperature": 0
            }
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"AI model failed: {str(error)}"
        )

    final_answer = response.message.content

    # Handle case where model returns no final answer
    if not final_answer:
        raise HTTPException(
            status_code=500,
            detail="The AI model did not generate a final answer."
        )

    return {
        "question": request.question,
        "document": request.document_name,
        "retrieved_chunks": len(retrieved_chunks),
        "context": context,
        "answer": final_answer
    }