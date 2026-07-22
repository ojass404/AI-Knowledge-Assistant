from backend.services.vectordb import search_documents

query = "What is Artificial Intelligence?"

results = search_documents(query)

print(results)