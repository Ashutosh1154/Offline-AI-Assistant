import chromadb
from pathlib import Path


BASE_DIRECTORY = Path(__file__).resolve().parent.parent

CHROMA_DIRECTORY = (
    BASE_DIRECTORY /
    "data" /
    "chroma_db"
)

CHROMA_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)


client = chromadb.PersistentClient(
    path=str(CHROMA_DIRECTORY)
)


collection = client.get_or_create_collection(
    name="offline_ai_documents"
)


# =========================================================
# SAVE DOCUMENT TO CHROMADB
# =========================================================

def save_to_chroma(
    document_name,
    embedded_chunks
):

    ids = []
    documents = []
    embeddings = []
    metadatas = []


    for index, chunk in enumerate(
        embedded_chunks
    ):

        chunk_id = (
            f"{document_name}_{index}"
        )


        ids.append(
            chunk_id
        )


        documents.append(
            chunk["text"]
        )


        embeddings.append(
            chunk["embedding"]
        )


        metadatas.append(
            {
                "document_name":
                    document_name,

                "chunk_index":
                    index
            }
        )


    # Remove previous chunks if the same
    # document was uploaded before.

    collection.delete(
        where={
            "document_name":
                document_name
        }
    )


    # Store updated document chunks.

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )


    return len(ids)


# =========================================================
# LIST DOCUMENTS
# =========================================================

def list_chroma_documents():

    results = collection.get(
        include=[
            "metadatas"
        ]
    )


    document_names = set()


    for metadata in results[
        "metadatas"
    ]:

        if (
            metadata
            and
            "document_name"
            in metadata
        ):

            document_names.add(
                metadata[
                    "document_name"
                ]
            )


    return sorted(
        document_names
    )


# =========================================================
# DELETE DOCUMENT
# =========================================================

def delete_chroma_document(
    document_name
):

    # Find chunks belonging to the
    # selected document.

    results = collection.get(
        where={
            "document_name":
                document_name
        }
    )


    chunk_ids = results.get(
        "ids",
        []
    )


    deleted_count = len(
        chunk_ids
    )


    if deleted_count == 0:

        return 0


    # Delete every ChromaDB chunk associated
    # with this document.

    collection.delete(
        where={
            "document_name":
                document_name
        }
    )


    return deleted_count