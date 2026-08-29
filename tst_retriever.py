from src.retriever import retrieve_chunks

results = retrieve_chunks(
    question="Definition of Artificial Intelligence",
    document_name="AI Notes",   # filename without .json
    top_k=3
)

print(f"Retrieved {len(results)} chunks.\n")

for i, chunk in enumerate(results, start=1):
    print(f"----- Chunk {i} -----")
    print("Similarity Score:", round(chunk["score"], 4))
    print(chunk["text"][:250])   # Print first 250 characters
    print()
