import os
import json
import uuid
from datetime import datetime
from PyPDF2 import PdfReader
from openai import OpenAI
import chromadb
from chromadb.config import Settings


client = OpenAI(api_key="")

# === Constants ===
PDF_FOLDER = "pdfs"
EMBEDDING_MODEL = "text-embedding-3-small"  # You can switch to "text-embedding-3-large" if needed
OUTPUT_JSONL = "fcc_embedding_payloads_rich_sourced.jsonl"

# === ChromaDB Client ===
chroma_client = chromadb.Client(Settings(anonymized_telemetry=False))
collection = chroma_client.get_or_create_collection(name="fcc_embeddings_rich_sourced")

# === Extract PDF Content in Chunks ===
def extract_text_chunks(file_path, max_tokens=800):
    """
    Extracts text from a PDF and splits it into smaller chunks.
    """
    try:
        reader = PdfReader(file_path)
        text_chunks = []
        chunk_text = ""
        page_num = 0

        for page in reader.pages:
            page_num += 1
            text = page.extract_text()
            if not text:
                continue
            for paragraph in text.split("\n\n"):
                paragraph = paragraph.strip()
                if len(chunk_text) + len(paragraph) < max_tokens:
                    chunk_text += " " + paragraph
                else:
                    text_chunks.append((chunk_text.strip(), page_num))
                    chunk_text = paragraph
        if chunk_text:
            text_chunks.append((chunk_text.strip(), page_num))
        return text_chunks
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return []

# === Generate Embedding ===
def get_embedding(text):
    """
    Generates an embedding for a given text using the OpenAI client.
    """
    try:
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Embedding error: {e}")
        return None

# === Process PDFs with Intelligent Source Detection ===
def process_documents(pdf_folder):
    payloads = []
    for file in os.listdir(pdf_folder):
        if file.lower().endswith(".pdf"):
            full_path = os.path.join(pdf_folder, file)
            stats = os.stat(full_path)
            doc_id = f"doc_{uuid.uuid4().hex[:6]}"
            date_now = datetime.now().strftime("%Y-%m-%d")

            try:
                reader = PdfReader(full_path)
                doc_info = reader.metadata
                page_count = len(reader.pages)
            except Exception:
                doc_info = {}
                page_count = 0

            # Intelligent Source Detection
            source = None
            if doc_info and doc_info.author and "fcc" in doc_info.author.lower():
                source = "FCC"
            elif doc_info and doc_info.producer and "government" in doc_info.producer.lower():
                source = "Government Agency"
            elif doc_info and doc_info.title and "scrape" in doc_info.title.lower():
                source = "Web Scrape"

            if not source:
                if "fcc" in file.lower():
                    source = "FCC"
                elif "scrape" in file.lower():
                    source = "Web Scrape"
                else:
                    source = "Unknown"

            base_metadata = {
    "document_id": doc_id,
    "title": doc_info.title if doc_info and doc_info.title else file.replace(".pdf", "").replace("_", " ").title(),
    "author": doc_info.author if doc_info and doc_info.author else "Unknown",
    "source": source,
    "date_created": datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d"),
    "date_uploaded": date_now,
    "file_type": "pdf",
    "language": "en",
    "tags": "emergency alerts, policy, regulatory",  # ✅ fixed here
    "summary": f"Document extracted from {file} containing emergency policy information.",
    "word_count": 0,
    "page_count": page_count,
    "document_category": "regulatory filing",
    "processing_status": "vectorized"
}


            chunks = extract_text_chunks(full_path)
            for i, (text, page_num) in enumerate(chunks):
                embedding = get_embedding(text)
                if embedding:
                    chunk_id = f"chunk_{str(i).zfill(3)}"
                    embedding_id = f"emb_{uuid.uuid4().hex[:6]}"
                    chunk_metadata = base_metadata.copy()
                    chunk_metadata.update({
                        "chunk_id": chunk_id,
                        "chunk_text": text,
                        "embedding_id": embedding_id,
                        "page_number": page_num,
                        "word_count": len(text.split())
                    })

                    record = {
                        "id": f"{doc_id}_{chunk_id}",
                        "text": text,
                        "embedding": embedding,
                        "metadata": chunk_metadata
                    }

                    payloads.append(record)

                    # Store in ChromaDB
                    collection.add(
                        documents=[text],
                        embeddings=[embedding],
                        metadatas=[chunk_metadata],
                        ids=[f"{doc_id}_{chunk_id}"]
                    )
    return payloads

# === Save to JSONL ===
def save_payloads_jsonl(payloads, out_path):
    """
    Saves the processed embedding payloads to a JSONL file.
    """
    with open(out_path, "w", encoding="utf-8") as f:
        for record in payloads:
            f.write(json.dumps(record) + "\n")
    print(f"✅ Saved full embedding records with intelligent source detection to {out_path}")

# === MAIN EXECUTION ===
if __name__ == "__main__":
    print("🔍 Creating FCC embeddings with intelligent source detection...")
    payloads = process_documents(PDF_FOLDER)
    save_payloads_jsonl(payloads, OUTPUT_JSONL)
    print("✅ Embedding + ChromaDB integration (rich + source-aware) complete.")
