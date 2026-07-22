from backend.services.embedding import generate_embedding

text = "Machine Learning is a branch of Artificial Intelligence."

vector = generate_embedding(text)

print("Vector Length:", len(vector))

print("\nFirst 10 Values:")

print(vector[:10])