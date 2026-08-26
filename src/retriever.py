import json
from pathlib import Path
from urllib import response

import numpy as np

from src.embedding_service import generate_embedding


EMBEDDING_DIRECTORY = Path("data/embeddings")


def cosine_similarity(vector1, vector2):

    vector1 = np.array(vector1)
    vector2 = np.array(vector2)

    similarity = np.dot(vector1, vector2) / (
        np.linalg.norm(vector1) * np.linalg.norm(vector2)
    )

    return similarity


def retrieve_chunks(question, document_name, top_k=3):

    question_embedding = generate_embedding(question)

    embedding_file = EMBEDDING_DIRECTORY / f"{document_name}.json"

    with open(embedding_file, "r", encoding="utf-8") as file:
        embedded_chunks = json.load(file)

    scored_chunks = []

    for chunk in embedded_chunks:

        score = cosine_similarity(
            question_embedding,
            chunk["embedding"]
        )

        scored_chunks.append(
            {
                "text": chunk["text"],
                "score": score
            }
        )

    scored_chunks.sort(
    key=lambda item: item["score"],
    reverse=True
)

    return scored_chunks[:top_k]
