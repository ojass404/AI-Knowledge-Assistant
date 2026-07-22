from sentence_transformers import SentenceTransformer

# Load the embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text):
    """
    Convert text into an embedding vector.
    """
    embedding = model.encode(text)
    return embedding.tolist()


def embed_chunks(chunks):
    """
    Generate embeddings for all chunks.
    """

    embedded_chunks = []

    for chunk in chunks:

        vector = generate_embedding(chunk["text"])

        embedded_chunks.append({

            "chunk_id": chunk["chunk_id"],

            "filename": chunk["filename"],

            "page": chunk["page"],

            "text": chunk["text"],

            "length": chunk["length"],

            "embedding": vector

        })

    return embedded_chunks