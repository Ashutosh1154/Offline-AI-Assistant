from fastapi import FastAPI, UploadFile, File
from app.schemas import QuestionRequest
import shutil
from pathlib import Path
from src.document_loader import load_pdf

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

    document_text = load_pdf(str(file_path))

    return {
        "message": "File uploaded and processed successfully",
        "filename": file.filename,
        "text_length": len(document_text)
    }