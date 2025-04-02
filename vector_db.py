import chromadb
import json
import os

# Ensure the embedding file exists
embedding_file = "corrected_embeddings.json"
if not os.path.exists(embedding_file):
    raise FileNotFoundError(f"Embedding file '{embedding_file}' not found.")

# Load embeddings and metadata from JSON file
with open(embedding_file, "r") as f:
    data = json.load(f)

# Extracting data
ids = [str(item["id"]) for item in data]  # Ensure IDs are strings
embeddings = [item["embedding"] for item in data]  # List of vectors
metadatas = [item["metadata"] for item in data]  # Metadata dictionary

# Initialize ChromaDB client with persistent storage
client = chromadb.PersistentClient(path="./chroma_db")

# Create or get the collection
collection = client.get_or_create_collection(name="embeddings_collection")

# Add data to ChromaDB
collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)

print(f"Successfully added {len(ids)} embeddings to ChromaDB.")

