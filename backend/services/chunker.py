def create_chunks(pages, filename, chunk_size=500, overlap=100):

    chunks = []

    for page in pages:

        text = page["text"]
        page_number = page["page"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk = text[start:end]

            chunks.append({

                "chunk_id": len(chunks) + 1,

                "filename": filename,

                "page": page_number,

                "text": chunk,

                "length": len(chunk)

            })

            start += chunk_size - overlap

    return chunks