import pymupdf
from pathlib import Path


PROCESSED_DIRECTORY = Path("data/processed")
PROCESSED_DIRECTORY.mkdir(parents=True, exist_ok=True)


def load_pdf(file_path):

    document = pymupdf.open(file_path)

    text = ""

    for page in document:

        page_text = page.get_text()

        text += page_text + "\n"

    document.close()

    return text.strip()


def save_text(document_name, text):

    output_file = (
        PROCESSED_DIRECTORY /
        f"{document_name}.txt"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(text)

    return output_file