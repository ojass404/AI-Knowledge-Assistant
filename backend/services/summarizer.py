from services.rag import ask_question


def summarize_document(summary_type: str = "bullet") -> dict:
    """
    Generate a summary of the uploaded document.

    Parameters
    ----------
    summary_type : str

        bullet
        paragraph
        executive

    Returns
    -------
    dict
    """

    if summary_type == "paragraph":

        instruction = """
Write a well-formatted paragraph summary.

Separate paragraphs with blank lines.
Keep the language simple and readable.
"""

    elif summary_type == "executive":

        instruction = """
Write an executive summary highlighting the most important points.
"""

    else:

        instruction = """
Summarize the document using Markdown.

Rules:
- Use bullet points.
- Put each point on a new line.
- Keep each bullet concise.
- Use headings if appropriate.
"""

    response = ask_question(instruction)

    if isinstance(response, dict):

        return response

    return {
        "answer": response,
        "sources": []
    }