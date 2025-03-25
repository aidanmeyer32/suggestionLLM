import os
from openai import OpenAI 
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Define the directories for text files and JSONL files
text_folder = 'text-files'
jsonl_folder = 'jsonl-files'

# Create the JSONL folder if it doesn't exist
if not os.path.exists(jsonl_folder):
    os.makedirs(jsonl_folder)

def generate_completions(text):
    """
    Generate completions from the given text using OpenAI API.

    Args:
        text (str): The input text to generate completions from.

    Returns:
        list: A list of completion strings.
    """
    # Initialize the text splitter with specified chunk size and overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,  # Added comma here
        chunk_overlap=200  # Overlap between chunks
    )
    # Split the input text into manageable chunks
    chunks = text_splitter.split_text(text)
    completions = []

    # Iterate over each chunk to generate completions
    for chunk in chunks:
        # Request completion from OpenAI API for each chunk
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "I am going to feed you chunks of text. Create a JSONL object from each chunk that will be used to fine-tune a GPT chat model. Each entry should be a complete and coherent piece of content.  Return the JSONL object, and nothing else. Ensure the JSON object is in the correct format for training a chat model.  Here is an example of the correct format for training a gpt chat model:  {\"messages\": [{\"role\": \"system\", \"content\": \"You are an AI assistant specialized in telecommunications and emergency alert systems.\"}, {\"role\": \"user\", \"content\": \"Can you explain the recent FCC regulations regarding Wireless Emergency Alerts (WEAs)?\"}, {\"role\": \"assistant\", \"content\": \"In October 2023, the Federal Communications Commission adopted rules requiring Participating Commercial Mobile Service (CMS) Providers to support Wireless Emergency Alerts in thirteen languages, in addition to English and American Sign Language. This was part of the FCC's effort to make emergency alerts more accessible to diverse populations. More details can be found in the 2023 WEA Accessibility Report and Order.\"}]} Your response should only contain the JSONL lines, and nothing else."},
                {"role": "user", "content": chunk}
            ],
            max_tokens=4000
        )
        # Extract and clean the completion text
        completion = response.choices[0].message.content.strip()
        # Append the completion to the list
        completions.append(completion)

    return completions

# Iterate through each file in the text folder
for text_file in os.listdir(text_folder):
    # Process only text files
    if text_file.endswith('.txt'):
        # Define paths for the text file and the corresponding JSONL file
        text_path = os.path.join(text_folder, text_file)
        jsonl_path = os.path.join(jsonl_folder, text_file.replace('.txt', '.jsonl'))
        
        # Skip if the JSONL file already exists
        if os.path.exists(jsonl_path):
            print(f"Skipping existing file: {jsonl_path}")
            continue

        # Process the file only if it doesn't exist
        with open(text_path, 'r', encoding='utf-8') as file:
            text = file.read()

        completions = generate_completions(text)

        with open(jsonl_path, 'w', encoding='utf-8') as jsonl_file:
            for completion in completions:
                jsonl_file.write(completion + '\n')

        print(f"Generated {jsonl_path}")