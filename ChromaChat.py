import json
import openai
from chromadb import PersistentClient

# === CONFIG ===
openai.api_key = openai_api_key  # 🔐 Replace with your OpenAI API key
persist_path = "./chroma_fcc_storage"
collection_name = "fcc_documents"
retrieval_limit = 5  # how many top results to use for context

# === INIT CHROMADB ===
client = PersistentClient(path=persist_path)
collection = client.get_or_create_collection(name=collection_name)

# === CHAT LOOP ===
print("🔊 FCC Regulatory Assistant (type 'exit' to quit)\n")

while True:
    user_query = input("👤 You: ")

    if user_query.lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break

    # Step 1: Embed the query with OpenAI
    embed_response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=user_query
    )
    query_vector = embed_response["data"][0]["embedding"]

    # Step 2: Query ChromaDB
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=retrieval_limit
    )

    # Step 3: Combine top chunks into context
    context_chunks = results['documents'][0]
    full_context = "\n\n".join(context_chunks)

    # Step 4: Send to OpenAI Chat
    prompt = f"""You are an expert assistant for regulatory and emergency communication policy. 
Using the following source material, answer the user's question in a clear, helpful way.

---SOURCE MATERIAL---
{full_context}

---USER QUESTION---
{user_query}
"""

    chat_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4"
        messages=[
            {"role": "system", "content": "You are a domain-specific assistant trained solely on emergency alert systems, public safety communications, cybersecurity policy, disaster response frameworks, and regulatory principles as defined in the embedded dataset. You must restrict your responses only to the information contained in the embedded data and refrain from generating answers outside this scope. Do not reference general knowledge, FCC responses, or unrelated domains (e.g., cooking, entertainment, etc.). Where relevant, relate insights strictly to ideas present in the embedded documents or clearly supported by them."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    # Step 5: Output the response
    answer = chat_response["choices"][0]["message"]["content"]
    print(f"\n🤖 FCC Bot: {answer}\n")
