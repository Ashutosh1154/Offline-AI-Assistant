from pathlib import Path

from src.chunking import chunk_text
from src.embedding_service import generate_chunk_embeddings
from src.vector_store import save_embeddings


# Read processed document
processed_file = Path("data/processed") / "AI Notes.txt"

text = processed_file.read_text(encoding="utf-8")

# Split document into chunks
chunks = chunk_text(text)

# Generate embeddings for each chunk
embedded_chunks = generate_chunk_embeddings(chunks)

# Save embeddings
output_file = save_embeddings("AI Notes", embedded_chunks)

print("Total Chunks:", len(chunks))

print("\nFirst Chunk Preview:\n")
print(chunks[0][:250])

print("\nEmbedding Dimensions:", len(embedded_chunks[0]["embedding"]))

print("\nFirst 5 Embedding Values:")
print(embedded_chunks[0]["embedding"][:5])

print("\nEmbeddings saved to:")
print(output_file)