import openai
import os 

# Initialize the OpenAI API Key
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API Key from environment variables
openai_api_key = os.getenv(openai_api_key)

if not openai_api_key:
    raise ValueError("OpenAI API Key not found in environment variables.")

openai.api_key = openai_api_key



response = openai.Completion.create(
    model="fine-tuned-davinci-2024-11-19",
    prompt="What is the emergency alert system?",
    max_tokens=100
)

print(response['choices'][0]['text'])
