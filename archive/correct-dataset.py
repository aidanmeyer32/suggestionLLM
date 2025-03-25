import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load the OpenAI API key from the environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def correct_jsonl_format(input_file: str, output_file: str):
    input_path = input_file
    output_path = output_file

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file '{input_file}' does not exist")

    try:
        with open(input_path, 'r', encoding='utf-8') as infile, \
             open(output_path, 'w', encoding='utf-8') as outfile:
            
            for line in infile:
                line = line.strip()
                
                if not line:  # Skip empty lines
                    continue
                
                try:
                    # Attempt to parse the line as JSON
                    json_obj = json.loads(line)
                    
                    # Ensure the JSON object is in the correct format for GPT chat model training
                    if isinstance(json_obj, dict) and "messages" in json_obj:
                        # Write the valid JSON object to the output file
                        outfile.write(json.dumps(json_obj) + '\n')
                    else:
                        # If the format is incorrect, use OpenAI API to correct it
                        response = client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": " Ensure the JSON object is in the correct format for training a chat model. Return the JSONL object, and nothing else. Here is an example of the correct format for training a gpt chat model:  {\"messages\": [{\"role\": \"system\", \"content\": \"You are an AI assistant specialized in telecommunications and emergency alert systems.\"}, {\"role\": \"user\", \"content\": \"Can you explain the recent FCC regulations regarding Wireless Emergency Alerts (WEAs)?\"}, {\"role\": \"assistant\", \"content\": \"In October 2023, the Federal Communications Commission adopted rules requiring Participating Commercial Mobile Service (CMS) Providers to support Wireless Emergency Alerts in thirteen languages, in addition to English and American Sign Language. This was part of the FCC's effort to make emergency alerts more accessible to diverse populations. More details can be found in the 2023 WEA Accessibility Report and Order.\"}]}"},
                                {"role": "user", "content": json.dumps(json_obj)}
                            ],
                            model="gpt-4o"
                        )
                        corrected_json = response.choices[0].message.content
                        outfile.write(corrected_json + '\n')
                
                except json.JSONDecodeError:
                    print(f"Invalid JSON: {line[:100]}...")
                
    except Exception as e:
        print(f"Critical error during processing: {str(e)}")
        raise

if __name__ == "__main__":
    input_file = "corrected-dataset.jsonl"
    output_file = "corrected-dataset2.jsonl"
    
    correct_jsonl_format(input_file, output_file)
    print("Process completed successfully")
