from ollama import chat

from services.vectordb import search_documents

conversation_history = []


def ask_question(question):

    global conversation_history

    results = search_documents(question)

    # -----------------------------
    # Build Context
    # -----------------------------

    context = ""

    for chunk in results:

        context += f"""
Document:
{chunk['filename']}

Page:
{chunk['page']}

Content:
{chunk['text']}

-----------------------------
"""

    # -----------------------------
    # Prompt
    # -----------------------------

    messages = [
    {
        "role": "system",
        "content": (
            """
You are an AI Knowledge Assistant.

Answer naturally.

Use only the retrieved context.

Do NOT answer in JSON unless the user explicitly asks for JSON.

Explain concepts in normal English.

Use bullet points when appropriate.
"""
        )
    }
]
    messages.extend(conversation_history)

    messages.append({

        "role": "user",

        "content": f"""
Context:

{context}

Question:

{question}
"""

    })

    response = chat(

        model="llama3.2",

        messages=messages

    )

    answer = response["message"]["content"]

    conversation_history.append({

        "role": "user",

        "content": question

    })

    conversation_history.append({

        "role": "assistant",

        "content": answer

    })

    return {

        "answer": answer,

        "sources": results

    }