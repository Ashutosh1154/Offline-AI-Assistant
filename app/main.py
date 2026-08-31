from pathlib import Path
import shutil

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from fastapi.staticfiles import (
    StaticFiles
)

from fastapi.responses import (
    FileResponse
)

from ollama import chat

from app.schemas import QuestionRequest

from src.document_loader import (
    save_text
)

from src.ocr_service import (
    extract_text_with_ocr
)

from src.chunking import (
    chunk_text
)

from src.embedding_service import (
    generate_chunk_embeddings
)

from src.chroma_store import (
    save_to_chroma,
    list_chroma_documents,
    delete_chroma_document
)

from src.chroma_retriever import (
    retrieve_from_chroma
)


# =========================================================
# CONFIGURATION
# =========================================================

MODEL_NAME = "qwen3:4b"


BASE_DIRECTORY = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


UPLOAD_DIRECTORY = (
    BASE_DIRECTORY /
    "data" /
    "uploads"
)


PROCESSED_DIRECTORY = (
    BASE_DIRECTORY /
    "data" /
    "processed"
)


FRONTEND_DIRECTORY = (
    BASE_DIRECTORY /
    "frontend"
)


UPLOAD_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)


PROCESSED_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Offline AI Assistant",
    version="2.0.0"
)


app.mount(
    "/static",

    StaticFiles(
        directory=str(
            FRONTEND_DIRECTORY
        )
    ),

    name="static"
)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return FileResponse(
        FRONTEND_DIRECTORY /
        "index.html"
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return {
        "status":
            "running",

        "model":
            MODEL_NAME
    }


# =========================================================
# UPLOAD DOCUMENT
# =========================================================

@app.post("/upload")
def upload_document(
    file: UploadFile = File(...)
):

    # -----------------------------------------------------
    # Validate file
    # -----------------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file was provided."
        )


    if not file.filename.lower().endswith(
        ".pdf"
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Only PDF files are supported."
            )
        )


    safe_filename = (
        Path(
            file.filename
        ).name
    )


    file_path = (
        UPLOAD_DIRECTORY /
        safe_filename
    )


    # -----------------------------------------------------
    # Save uploaded PDF
    # -----------------------------------------------------

    try:

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to save PDF: "
                f"{str(error)}"
            )
        )


    # -----------------------------------------------------
    # Extract text / OCR
    # -----------------------------------------------------

    try:

        (
            document_text,
            ocr_pages
        ) = extract_text_with_ocr(
            file_path
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Document extraction "
                "failed: "
                f"{str(error)}"
            )
        )


    if not document_text.strip():

        raise HTTPException(
            status_code=422,
            detail=(
                "No readable text could "
                "be extracted from the PDF."
            )
        )


    # -----------------------------------------------------
    # Save extracted text
    # -----------------------------------------------------

    try:

        save_text(
            file_path.stem,
            document_text
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to save extracted "
                "text: "
                f"{str(error)}"
            )
        )


    # -----------------------------------------------------
    # Chunk text
    # -----------------------------------------------------

    chunks = chunk_text(
        document_text
    )


    if not chunks:

        raise HTTPException(
            status_code=422,
            detail=(
                "No text chunks could "
                "be created."
            )
        )


    # -----------------------------------------------------
    # Generate embeddings
    # -----------------------------------------------------

    try:

        embedded_chunks = (
            generate_chunk_embeddings(
                chunks
            )
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Embedding generation "
                "failed: "
                f"{str(error)}"
            )
        )


    # -----------------------------------------------------
    # Store in ChromaDB
    # -----------------------------------------------------

    try:

        stored_chunks = (
            save_to_chroma(
                file_path.stem,
                embedded_chunks
            )
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "ChromaDB storage failed: "
                f"{str(error)}"
            )
        )


    # -----------------------------------------------------
    # Return upload information
    # -----------------------------------------------------

    return {
        "message":
            "File uploaded and indexed successfully",

        "filename":
            file.filename,

        "document_name":
            file_path.stem,

        "text_length":
            len(document_text),

        "chunks_created":
            len(chunks),

        "chroma_chunks_stored":
            stored_chunks,

        "ocr_used":
            ocr_pages > 0,

        "ocr_pages":
            ocr_pages
    }


# =========================================================
# LIST DOCUMENTS
# =========================================================

@app.get("/documents")
def list_documents():

    try:

        documents = (
            list_chroma_documents()
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to retrieve "
                "documents: "
                f"{str(error)}"
            )
        )


    return {
        "documents":
            documents
    }


# =========================================================
# DELETE DOCUMENT
# =========================================================

@app.delete(
    "/documents/{document_name}"
)
def delete_document(
    document_name: str
):

    document_name = (
        document_name.strip()
    )


    if not document_name:

        raise HTTPException(
            status_code=400,
            detail=(
                "Document name cannot "
                "be empty."
            )
        )


    # -----------------------------------------------------
    # Verify document exists
    # -----------------------------------------------------

    try:

        available_documents = (
            list_chroma_documents()
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to access "
                "ChromaDB: "
                f"{str(error)}"
            )
        )


    if (
        document_name
        not in available_documents
    ):

        raise HTTPException(
            status_code=404,
            detail=(
                "Document was not found."
            )
        )


    # -----------------------------------------------------
    # Delete from ChromaDB
    # -----------------------------------------------------

    try:

        deleted_chunks = (
            delete_chroma_document(
                document_name
            )
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to delete document "
                "from ChromaDB: "
                f"{str(error)}"
            )
        )


    # -----------------------------------------------------
    # Delete uploaded PDF
    # -----------------------------------------------------

    for pdf_file in (
        UPLOAD_DIRECTORY.glob(
            "*.pdf"
        )
    ):

        if (
            pdf_file.stem
            == document_name
        ):

            try:

                pdf_file.unlink()

            except OSError:

                pass


    # -----------------------------------------------------
    # Delete processed text
    # -----------------------------------------------------

    processed_file = (
        PROCESSED_DIRECTORY /
        f"{document_name}.txt"
    )


    if processed_file.exists():

        try:

            processed_file.unlink()

        except OSError:

            pass


    return {
        "message":
            "Document deleted successfully",

        "document":
            document_name,

        "deleted_chunks":
            deleted_chunks
    }


# =========================================================
# ASK QUESTION
# =========================================================

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
        available_documents = list_chroma_documents()

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
        retrieved_chunks = retrieve_from_chroma(
            question=question,
            document_name=document_name,
            top_k=3
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"ChromaDB retrieval failed: {str(error)}"
        )

    if not retrieved_chunks:
        raise HTTPException(
            status_code=404,
            detail=(
                "No relevant information was found "
                "in the selected document."
            )
        )

    context = "\n\n".join(
        chunk["text"]
        for chunk in retrieved_chunks
    )

    system_prompt = """
You are an offline document question-answering assistant.

Use only the information provided in the document context.

Return only the final answer.

Do not show analysis, reasoning, planning, thought process,
intermediate steps, or internal reasoning.

Do not mention the context, prompt, chunks, or instructions.

Answer directly using clear and complete sentences.

Keep the answer concise but complete.

If the answer is not available in the document, respond exactly:

The answer is not available in the uploaded document.
"""

    user_prompt = f"""
DOCUMENT CONTEXT:

{context}

QUESTION:

{question}

/no_think
"""

    try:
        response = chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            think=False,
            options={
                "temperature": 0,
                "num_predict": 800
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

    if "</think>" in final_answer:
        final_answer = (
            final_answer
            .split("</think>", 1)[1]
            .strip()
        )

    if final_answer.startswith("<think>"):
        final_answer = (
            final_answer
            .replace("<think>", "", 1)
            .strip()
        )

    if not final_answer:
        raise HTTPException(
            status_code=500,
            detail="The AI model did not generate an answer."
        )

    return {
        "question": question,
        "document": document_name,
        "retrieved_chunks": len(retrieved_chunks),
        "answer": final_answer
    }