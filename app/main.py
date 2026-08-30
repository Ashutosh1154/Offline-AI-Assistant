from pathlib import Path
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from ollama import chat

from app.schemas import QuestionRequest
from src.document_loader import save_text
from src.ocr_service import extract_text_with_ocr
from src.chunking import chunk_text
from src.embedding_service import generate_chunk_embeddings
from src.chroma_store import save_to_chroma, list_chroma_documents
from src.chroma_retriever import retrieve_from_chroma


MODEL_NAME = "qwen3:4b"

BASE_DIRECTORY = Path(__file__).resolve().parent.parent
UPLOAD_DIRECTORY = BASE_DIRECTORY / "data" / "uploads"
FRONTEND_DIRECTORY = BASE_DIRECTORY / "frontend"

UPLOAD_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)

app = FastAPI(
    title="Offline AI Assistant",
    version="1.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIRECTORY)),
    name="static"
)


@app.get("/")
def home():
    return FileResponse(
        FRONTEND_DIRECTORY / "index.html"
    )


@app.get("/health")
def health():
    return {
        "status": "running",
        "model": MODEL_NAME
    }


@app.post("/upload")
def upload_document(
    file: UploadFile = File(...)
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was provided."
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    file_path = (
        UPLOAD_DIRECTORY /
        Path(file.filename).name
    )

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save PDF: {str(error)}"
        )

    try:
        document_text, ocr_pages = (
            extract_text_with_ocr(
                file_path
            )
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Document extraction failed: {str(error)}"
        )

    if not document_text.strip():
        raise HTTPException(
            status_code=422,
            detail="No readable text could be extracted from the PDF."
        )

    try:
        save_text(
            file_path.stem,
            document_text
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save extracted text: {str(error)}"
        )

    chunks = chunk_text(
        document_text
    )

    if not chunks:
        raise HTTPException(
            status_code=422,
            detail="No text chunks could be created."
        )

    try:
        embedded_chunks = (
            generate_chunk_embeddings(
                chunks
            )
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Embedding generation failed: {str(error)}"
        )

    try:
        stored_chunks = save_to_chroma(
            file_path.stem,
            embedded_chunks
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"ChromaDB storage failed: {str(error)}"
        )

    return {
        "message": "File uploaded and indexed successfully",
        "filename": file.filename,
        "document_name": file_path.stem,
        "text_length": len(document_text),
        "chunks_created": len(chunks),
        "chroma_chunks_stored": stored_chunks,
        "ocr_used": ocr_pages > 0,
        "ocr_pages": ocr_pages
    }


@app.get("/documents")
def list_documents():

    try:
        documents = list_chroma_documents()

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve documents: {str(error)}"
        )

    return {
        "documents": documents
    }


@app.post("/ask")
def ask_question(
    request: QuestionRequest
):

    question = request.question.strip()
    document_name = request.document_name.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    if not document_name:
        raise HTTPException(
            status_code=400,
            detail="Document name cannot be empty."
        )

    try:
        available_documents = (
            list_chroma_documents()
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to access ChromaDB: {str(error)}"
        )

    if document_name not in available_documents:
        raise HTTPException(
            status_code=404,
            detail="Selected document was not found."
        )

    try:
        retrieved_chunks = (
            retrieve_from_chroma(
                question=question,
                document_name=document_name,
                top_k=2
            )
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"ChromaDB retrieval failed: {str(error)}"
        )

    if not retrieved_chunks:
        raise HTTPException(
            status_code=404,
            detail="No relevant information was found in the selected document."
        )

    context = "\n\n".join(
        chunk["text"]
        for chunk in retrieved_chunks
    )

    prompt = f"""
You are an offline document-based AI assistant.

Answer the QUESTION using only the provided CONTEXT.

Rules:
1. Use only information available in the CONTEXT.
2. Do not use outside knowledge.
3. Do not invent or assume information.
4. Return only the final answer.
5. Do not show or explain your reasoning.
6. Do not mention the context or these instructions.
7. Answer using complete sentences.
8. Give enough detail to fully answer the question without unnecessary information.
9. Prefer 1 to 4 sentences depending on the question.
10. If the answer is unavailable, return exactly:
The answer is not available in the uploaded document.

CONTEXT:
{context}

QUESTION:
{question}

FINAL ANSWER:
"""

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

    final_answer = (
        response.message.content or ""
    ).strip()

    if not final_answer:

        try:
            retry_response = chat(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                think=True,
                options={
                    "num_predict": 4000,
                    "temperature": 0
                }
            )

        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=f"AI model retry failed: {str(error)}"
            )

        final_answer = (
            retry_response.message.content or ""
        ).strip()

    if not final_answer:
        raise HTTPException(
            status_code=500,
            detail="The AI model did not generate a final answer."
        )

    return {
        "question": question,
        "document": document_name,
        "retrieved_chunks": len(
            retrieved_chunks
        ),
        "answer": final_answer
    }