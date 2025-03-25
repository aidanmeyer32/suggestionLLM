#This script will scrape all pdf documents in /pdf-docs and save each one to a text file with the same name in /text-files. 

import os
import requests
from PyPDF2 import PdfReader
import io

pdf_folder = 'pdf-docs'
text_folder = 'text-files'

# Create the text folder if it doesn't exist
if not os.path.exists(text_folder):
    os.makedirs(text_folder)

# Iterate through each file in the PDF folder
for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith('.pdf'):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        text_path = os.path.join(text_folder, pdf_file.replace('.pdf', '.txt'))
        
        # Read each file and write to .txt 
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            with open(text_path, 'w', encoding='utf-8') as text_file:
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    text_file.write(text)
