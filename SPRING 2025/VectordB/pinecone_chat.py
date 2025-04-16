import streamlit as st
from openai import OpenAI
from pinecone import Pinecone

# === Load secrets ===
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
pc = Pinecone(api_key=st.secrets["PINECONE_API_KEY"])
index = pc.Index("fcc-chatbot-index")

# === UI ===
st.title("Emergency Alerting Systems and Reliability Chatbot")
query = st.text_input("💬 Ask a question:")

if query:
    with st.spinner("🔍 Searching Pinecone..."):

        # Step 1: Embed query
        embed_response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=[query]
        )
        query_vector = embed_response.data[0].embedding

        # Step 2: Search Pinecone with larger top_k
        results = index.query(
            vector=query_vector,
            top_k=15,  # try a larger pool to choose from
            include_metadata=True
        )
        raw_chunks = [match["metadata"]["text"] for match in results["matches"]]

    with st.spinner("🧠 Re-ranking with GPT..."):

        # Step 3: Ask GPT to rank the chunks
        ranking_prompt = f"""You are helping with a research assistant. The user has asked a question:
        
"{query}"

Here are 15 content chunks retrieved from a database. Please select and return the 3 most relevant ones (verbatim) based on how well they answer the question. Return only the text chunks, no explanations.

--- CHUNKS ---
{chr(10).join(f"- {chunk}" for chunk in raw_chunks)}
"""

        reranked_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": ranking_prompt}],
            temperature=0.2
        )
        top_chunks = reranked_response.choices[0].message.content

    with st.spinner("💬 Generating answer..."):

        final_prompt = f"""Using the following carefully selected source material, answer the user's question.

---SOURCE MATERIAL---
{top_chunks}

---QUESTION---
{query}
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a domain-specific assistant trained solely on emergency alert systems, public safety communications, cybersecurity policy, disaster response frameworks, and regulatory principles as defined in the embedded dataset. You must restrict your responses only to the information contained in the embedded data and refrain from generating answers outside this scope. Do not reference general knowledge, FCC responses, or unrelated domains (e.g., cooking, entertainment, etc.). Where relevant, relate insights strictly to ideas present in the embedded documents or clearly supported by them."},
                {"role": "user", "content": final_prompt}
            ],
            temperature=0.3
        )
        answer = response.choices[0].message.content
        st.markdown("### 🤖 Response")
        st.write(answer)

        with st.expander("📄 GPT-selected chunks"):
            st.text(top_chunks)