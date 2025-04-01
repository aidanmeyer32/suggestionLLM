import json
import openai
from chromadb import PersistentClient

# === CONFIG ===
openai.api_key = "API KEY"  # Replace this with your actual key
embedding_file = "fcc_embedding_payloads_rich_sourced.jsonl"
persist_path = "./chroma_fcc_storage"
collection_name = "fcc_documents"

# === 1. Initialize ChromaDB ===
client = PersistentClient(path=persist_path)
collection = client.get_or_create_collection(name=collection_name)

# === 2. Load and Add Documents (Skip duplicates automatically) ===
with open(embedding_file, "r", encoding="utf-8") as f:
    lines = [json.loads(line) for line in f]

# Prepare data
ids, documents, metadatas, embeddings = [], [], [], []

for entry in lines:
    ids.append(entry["id"])
    documents.append(entry["text"])
    metadatas.append(entry.get("metadata", {}))
    embeddings.append(entry["embedding"])

try:
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )
    print(f"✅ Successfully added {len(ids)} documents to ChromaDB.")
except Exception as e:
    print("⚠️ Some or all documents already exist in the collection. Skipping re-insertion.")

# === 3. Query using OpenAI Embeddings ===
query = "public warning systems and wireless emergency alerts"

# Embed query using the same model used for stored documents
response = openai.Embedding.create(
    model="text-embedding-ada-002",
    input=query
)
query_vector = response['data'][0]['embedding']

# Run the query
results = collection.query(
    query_embeddings=[query_vector],
    n_results=5
)

# === 4. Display Results ===
print(f"\n🔍 Top 5 matches for query: '{query}'")
for i, doc in enumerate(results['documents'][0]):
    print(f"\n🔹 Match {i+1}:")
    print("Text:", doc[:300] + "..." if len(doc) > 300 else doc)
    print("Metadata:", results['metadatas'][0][i])
