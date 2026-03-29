import fitz

def parse_pdf(file_path):

    doc = fitz.open(file_path)

    text_data = []
    table_data = []
    image_data = []

    for page_num, page in enumerate(doc):

        text = page.get_text()

        if text.strip():
            text_data.append({
                "content": text,
                "page": page_num,
                "type": "text"
            })

        # Simple table detection
        if "Table" in text or "|" in text:
            table_data.append({
                "content": text,
                "page": page_num,
                "type": "table"
            })

        images = page.get_images(full=True)

        for img in images:
            xref = img[0]
            base_image = doc.extract_image(xref)

            image_data.append({
                "image": base_image["image"],
                "page": page_num,
                "type": "image"
            })

    return text_data, table_data, image_data