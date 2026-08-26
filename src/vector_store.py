import json
from pathlib import Path

EMBEDDING_DIRECTORY = Path("data/embeddings")
EMBEDDING_DIRECTORY.mkdir(parents=True, exist_ok=True)


def save_embeddings(document_name, embedded_chunks):

    output_file = EMBEDDING_DIRECTORY / f"{document_name}.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(embedded_chunks, file, ensure_ascii=False, indent=4)

    return output_file