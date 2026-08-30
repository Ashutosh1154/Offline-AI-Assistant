import chromadb
from pathlib import Path


CHROMA_DIRECTORY = Path("data/chroma_db")

client = chromadb.PersistentClient(
    path=str(CHROMA_DIRECTORY)
)

collection = client.get_or_create_collection(
    name="offline_ai_documents"
)


def save_to_chroma(document_name, embedded_chunks):

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for index, chunk in enumerate(embedded_chunks):

        chunk_id = f"{document_name}_{index}"

        ids.append(chunk_id)

        documents.append(
            chunk["text"]
        )

        embeddings.append(
            chunk["embedding"]
        )

        metadatas.append(
            {
                "document_name": document_name,
                "chunk_index": index
            }
        )

    # Remove previous chunks for same document
    collection.delete(
        where={
            "document_name": document_name
        }
    )

    # Save new chunks
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(ids)


def list_chroma_documents():

    results = collection.get(
        include=["metadatas"]
    )

    document_names = set()

    for metadata in results["metadatas"]:

        if metadata and "document_name" in metadata:
            document_names.add(
                metadata["document_name"]
            )

    return sorted(document_names)