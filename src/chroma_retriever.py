from src.embedding_service import generate_embedding
from src.chroma_store import collection


def retrieve_from_chroma(question, document_name, top_k=3):

    question_embedding = generate_embedding(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
        where={
            "document_name": document_name
        }
    )

    retrieved_chunks = []

    if not results["documents"]:
        return retrieved_chunks

    documents = results["documents"][0]
    distances = results["distances"][0]

    for document, distance in zip(documents, distances):

        retrieved_chunks.append(
            {
                "text": document,
                "distance": distance
            }
        )

    return retrieved_chunks
