from src.chunking import chunk_text
from src.embedding_service import generate_chunk_embeddings
from src.chroma_store import save_to_chroma


text = """
Artificial Intelligence is the simulation of human intelligence
processes by machines.

Machine Learning is a branch of Artificial Intelligence.

OCR stands for Optical Character Recognition.
"""

chunks = chunk_text(text)

embedded_chunks = generate_chunk_embeddings(
    chunks
)

stored_chunks = save_to_chroma(
    "test_document",
    embedded_chunks
)

print("Chunks stored in ChromaDB:", stored_chunks)
