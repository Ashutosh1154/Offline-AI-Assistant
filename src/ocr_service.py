import pymupdf


def extract_text_with_ocr(file_path):

    document = pymupdf.open(file_path)

    extracted_text = ""
    ocr_pages = 0

    for page in document:

        # Try normal extraction first
        page_text = page.get_text().strip()

        # If very little text exists,
        # treat this page as scanned
        if len(page_text) < 50:

            text_page = page.get_textpage_ocr(
                language="eng",
                dpi=300,
                full=True
            )

            page_text = page.get_text(
                textpage=text_page
            ).strip()

            ocr_pages += 1

        extracted_text += page_text + "\n\n"

    document.close()

    return extracted_text.strip(), ocr_pages