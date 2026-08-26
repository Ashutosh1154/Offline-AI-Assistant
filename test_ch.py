
from src.chunking import chunk_text

text = """
Machine learning is a branch of artificial intelligence.
It allows computers to learn patterns from data.
Deep learning is a subset of machine learning.
Neural networks are commonly used in deep learning.
"""

chunks = chunk_text(text, chunk_size=100, overlap=20)

print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i + 1} ---")
    print(chunk)
