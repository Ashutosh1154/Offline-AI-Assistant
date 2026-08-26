from pathlib import Path

from src.chunking import chunk_text
from src.embedding_service import generate_chunk_embeddings
from src.vector_store import save_embeddings

processed_file = Path("data/processed") / "rmt5&6.txt"

text = processed_file.read_text(encoding="utf-8")

chunks = chunk_text(text)

embedded_chunks = generate_chunk_embeddings(chunks)

saved_file = save_embeddings(processed_file.stem, embedded_chunks)

print("Embeddings saved to:", saved_file)