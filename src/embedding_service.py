
from ollama import embed


EMBEDDING_MODEL = "nomic-embed-text"


def generate_embedding(text):

    response = embed(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response["embeddings"][0]

def generate_chunk_embeddings(chunks):

    embedded_chunks = []

    for chunk in chunks:

        embedding = generate_embedding(chunk)

        embedded_chunks.append(
            {
                "text": chunk,
                "embedding": embedding
            }
        )

    return embedded_chunks
