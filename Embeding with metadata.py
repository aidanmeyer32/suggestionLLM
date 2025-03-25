import os
import json
import fitz  # PyMuPDF for extracting PDF metadata
import numpy as np
from sentence_transformers import SentenceTransformer

# Function to extract metadata from a PDF file
def extract_pdf_metadata(pdf_file_path):
    try:
        doc = fitz.open(pdf_file_path)
        metadata = doc.metadata  # Returns a dictionary with metadata info
        metadata.pop('creationDate', None)  
        metadata.pop('modDate', None)  
        metadata.pop('format', None)
        metadata.pop('trapped', None)
        metadata.pop('encryption', None)
        metadata.pop('producer', None)
        metadata.pop('creator', None)
        
        return metadata
    except Exception as e:
        print(f"Error extracting metadata from {pdf_file_path}: {e}")
        return None

# Path to the folder containing PDF files
folder_path = '/Users/folder'  

# Initialize a list to hold metadata for all files
metadata_list = []

# Iterate over each file in the folder
for filename in os.listdir(folder_path):
    # Only process PDF files 
    if filename.endswith('.pdf'):
        pdf_file_path = os.path.join(folder_path, filename)

        # Extract metadata for each PDF file
        pdf_metadata = extract_pdf_metadata(pdf_file_path)

        if pdf_metadata:
            metadata = {
                "document_id": filename,  
                "pdf_metadata": pdf_metadata  # Include the PDF metadata extracted
            }
            metadata_list.append(metadata)

# Initialize the SentenceTransformer model for embedding generation
model = SentenceTransformer('all-MiniLM-L6-v2')

# Prepare a list to store the embeddings along with metadata
embeddings_list = []

# Function to extract text from PDF using PyMuPDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)  # Open the PDF
    text = ""
    for page_num in range(doc.page_count):  # Iterate through all pages
        page = doc.load_page(page_num)  # Get a page
        text += page.get_text()  # Extract text from the page
    return text

# Process each metadata entry and generate embeddings
for metadata in metadata_list:
    document_id = metadata.get('document_id')
    pdf_path = os.path.join(folder_path, document_id)  

    # Extract the text from the PDF
    document_text = extract_text_from_pdf(pdf_path)

    # Generate the embedding for the document text
    embedding = model.encode(document_text).tolist()  

    # Append both the metadata and embedding to the list
    embeddings_list.append({
        'document_id': document_id,
        'metadata': metadata,  # Include all metadata for the document
        'embedding': embedding
    })

print("Embeddings with metadata have been generated and are available in memory.")
