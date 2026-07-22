from backend.services.vectordb import show_all

data = show_all()

print(data.keys())

print("\nTotal Documents:", len(data["documents"]))

print("\nFirst Document:")

print(data["documents"][0])