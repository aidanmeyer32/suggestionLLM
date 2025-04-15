import json
from pinecone import Pinecone, ServerlessSpec

# === CONFIG ===
api_key = ""           # 🔐 Replace this
env_region = "gcp-starter"                  # 🔐 Replace with your region
index_name = "fcc-chatbot-index"

# === Connect to Pinecone ===
pc = Pinecone(api_key=api_key)

# === Check if index exists, or connect to it ===
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric='cosine',
        spec=ServerlessSpec(cloud='gcp', region=env_region.split("-")[0])
    )

index = pc.Index(index_name)

# === Load your precomputed embeddings ===
with open("fcc_embedding_payloads_rich_sourced.jsonl", "r", encoding="utf-8") as f:
    records = [json.loads(line) for line in f]

# === Upload in batches ===
batch_size = 50
for i in range(0, len(records), batch_size):
    batch = records[i:i+batch_size]
    vectors = []
    for item in batch:
        vectors.append((
            item["id"],
            item["embedding"],
            {"text": item["text"]}  # Adjust field name if needed
        ))
    index.upsert(vectors)

print("✅ Successfully uploaded embeddings to Pinecone!")
