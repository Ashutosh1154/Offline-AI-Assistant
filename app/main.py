from fastapi import FastAPI, UploadFile, File
from app.schemas import QuestionRequest
import shutil
from pathlib import Path
from src.document_loader import load_pdf, save_text
from ollama import chat

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
def ask_question(request:QuestionRequest):
    processed_directory = Path("data/processed")
    processed_files = sorted(processed_directory.glob("*.txt"))

    if not processed_files:
            return {
        "error": "No processed document found. Please upload a PDF first."
    }

    processed_file = processed_files[-1]
    with open(processed_file, "r", encoding="utf-8") as file:
            document_text=file.read()

    prompt= f"""
        You are an AI Assistant
        Answer the user's questions using the information from the document below.
        Document:
        {document_text}

        Question:
        {request.question}
        """

    response= chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        )

    return {
        "question": request.question,
        "answer":response.message.content
    }