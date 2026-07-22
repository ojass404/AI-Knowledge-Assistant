import fitz


def extract_text(pdf_path):
    """
    Extract text page by page from a PDF.

    Parameters
    ----------
    pdf_path : str
        Path to the PDF file.

    Returns
    -------
    list
        A list of dictionaries.
    """

    document = fitz.open(pdf_path)

    pages = []

    for page_number in range(len(document)):

        page = document.load_page(page_number)

        text = page.get_text()

        pages.append(
            {
                "page": page_number + 1,
                "text": text
            }
        )

    document.close()

    return pages