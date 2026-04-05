import fitz  # PyMuPDF


def parse_pdf(file_path: str):
    doc = fitz.open(file_path)

    text_chunks = []
    table_chunks = []
    image_chunks = []

    for page_num, page in enumerate(doc):
        page_number = page_num + 1

        # -------- TEXT EXTRACTION --------
        text = page.get_text("text")

        if text and len(text.strip()) > 50:
            text_chunks.append({
                "content": text,
                "page": page_number,
                "type": "text"
            })

        # -------- TABLE DETECTION (IMPROVED) --------
        blocks = page.get_text("blocks")

        for block in blocks:
            block_text = block[4]

            # heuristic for table-like content
            if (
                "|" in block_text or
                "\t" in block_text or
                "  " in block_text and len(block_text.split()) > 5
            ):
                table_chunks.append({
                    "content": block_text,
                    "page": page_number,
                    "type": "table"
                })

        # -------- IMAGE EXTRACTION --------
        images = page.get_images(full=True)

        for img in images:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            image_chunks.append({
                "image_bytes": image_bytes,
                "page": page_number,
                "type": "image"
            })

    return text_chunks, table_chunks, image_chunks