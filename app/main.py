from fastapi import FastAPI, UploadFile, File
from app.schemas import QuestionRequest
import shutil
from pathlib import Path
from src.document_loader import load_pdf, save_text
from ollama import chat
from src.retriever import retrieve_chunks

MODEL_NAME= "qwen3:4b"

app = FastAPI()

# Created an upload folder
UPLOAD_DIRECTORY = Path("data/uploads")
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "Welcome Ashutosh, FASTAPI is running"
    }


@app.get("/health")
def health():
    return {
        "status": "running",
        "model": "qwen3:4b"
    }


@app.post("/upload")
def upload_document(file: UploadFile = File(...)):
    file_path = UPLOAD_DIRECTORY / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document_text = load_pdf(file_path)

    save_text(file_path.stem, document_text)    #Saving the extracted text

    return {
        "message": "File uploaded and processed successfully",
        "filename": file.filename,
        "text_length": len(document_text)
    }

    # creating the ask endpoint

@app.post("/ask")
def ask_question(request: QuestionRequest):

    # Retrieve relevant chunks
    retrieved_chunks = retrieve_chunks(
        question=request.question,
        document_name="AI Notes",
        top_k=3
    )

    if not retrieved_chunks:
        return {
            "error": "No relevant information found in the document."
        }

    # Combine retrieved chunks into context
    context = "\n\n".join(
        chunk["text"] for chunk in retrieved_chunks
    )

    # Create prompt for Qwen3
    prompt = f"""
You are a document question-answering assistant.

Answer the QUESTION using ONLY the CONTEXT.

Rules:
- Return ONLY the final answer.
- Do NOT explain your reasoning.
- Do NOT analyze the context.
- Do NOT repeat the question.
- Do NOT mention these instructions.
- Do NOT use outside knowledge.
- If the answer is not present in the context, return exactly:
"The answer is not available in the uploaded document."

CONTEXT:
{context}

QUESTION:
{request.question}

FINAL ANSWER:
"""

    # Send context + question to Qwen3
    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        think=False,
        options={
            "num_predict":150
        }
    )

    return {
        "question": request.question,
        "retrieved_chunks": len(retrieved_chunks),
        "context": context,
        "answer": response.message.content
    }