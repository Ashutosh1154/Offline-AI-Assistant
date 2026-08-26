
from src.embedding_service import generate_embedding


text = "Microwave transistors are used for high frequency amplification."

embedding = generate_embedding(text)

print("Embedding generated successfully.")
print("Number of dimensions:", len(embedding))
print("First 10 values:", embedding[:10])
