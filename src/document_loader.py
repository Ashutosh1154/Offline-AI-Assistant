
import pymupdf
from pathlib import Path
from src.ocr_service import extract_text_from_image

TEMP_IMAGE_DIRECTORY = Path("data/processed/page_images")

TEMP_IMAGE_DIRECTORY.mkdir(parents=True, exist_ok=True)

def load_pdf(file_path):

    document = pymupdf.open(file_path)

    extracted_text = ""

    for page_number, page in enumerate(document):

        page_text = page.get_text().strip()

        if page_text:
            extracted_text += page_text + "\n\n"

    else:
        print(f"OCR running on Page {page_number + 1}")

        pixmap = page.get_pixmap()

        image_path = TEMP_IMAGE_DIRECTORY / f"page_{page_number + 1}.png"

        pixmap.save(image_path)

        ocr_text = extract_text_from_image(image_path)

        extracted_text += ocr_text + "\n\n"

    document.close()
    return extracted_text.strip()

def save_text(file_name, text):

        output_path = Path("data/processed") / f"{file_name}.txt"

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(text)

        return output_path
