from backend.services.rag import ask_llm
context = """
Machine Learning is a subset of Artificial Intelligence.

It learns patterns from data.
"""

question = "What is Machine Learning?"
answer = ask_llm(context, question)
print(answer)