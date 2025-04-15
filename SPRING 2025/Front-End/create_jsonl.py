import fitz  # PyMuPDF
import json
import os

# === Configuration ===
INPUT_PDF_DIR = "pdf/"
OUTPUT_JSONL_DIR = "frontend/jsonl_outputs/"
os.makedirs(OUTPUT_JSONL_DIR, exist_ok=True)

SYSTEM_PROMPT = (
    "You are an AI assistant trained to provide expert-level insights on emergency alert systems, "
    "cybersecurity, public safety communications, and telecommunications policy. Be clear, cite sources where relevant, "
    "and prioritize user safety and practical solutions."
)

# === PDF Text Extraction ===
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

# === Placeholder Q&A Parser ===
def generate_prompt_response_pairs(text):
    pairs = []
    chunks = text.split("Q:")
    for chunk in chunks[1:]:
        try:
            question, answer = chunk.split("A:", 1)
            pairs.append({
                "prompt": question.strip(),
                "response": answer.strip()
            })
        except ValueError:
            continue
    return pairs

# === Write JSONL File for Each PDF ===
def write_individual_jsonl(pairs, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for pair in pairs:
            json_obj = {
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": pair["prompt"]},
                    {"role": "assistant", "content": pair["response"]}
                ]
            }
            f.write(json.dumps(json_obj) + "\n")
    print(f"✅ Created: {output_path}")

# === Main Workflow ===
def main():
    for filename in os.listdir(INPUT_PDF_DIR):
        if filename.endswith(".pdf"):
            base_name = os.path.splitext(filename)[0]
            output_file = os.path.join(OUTPUT_JSONL_DIR, f"{base_name}.jsonl")

            pdf_path = os.path.join(INPUT_PDF_DIR, filename)
            print(f"📄 Processing: {filename}")
            text = extract_text_from_pdf(pdf_path)
            pairs = generate_prompt_response_pairs(text)

            if pairs:
                write_individual_jsonl(pairs, output_file)
            else:
                print(f"⚠️ Skipped {filename} — no valid Q&A pairs found.")

if __name__ == "__main__":
    main()
