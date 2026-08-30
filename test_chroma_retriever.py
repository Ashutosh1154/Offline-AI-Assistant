from src.chroma_retriever import retrieve_from_chroma


results = retrieve_from_chroma(
    question="What does OCR stand for?",
    document_name="test_document",
    top_k=3
)

print("Retrieved chunks:", len(results))

for index, chunk in enumerate(results, start=1):

    print(f"\n--- Chunk {index} ---")
    print("Distance:", chunk["distance"])
    print(chunk["text"])
