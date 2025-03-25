import os
from openai import OpenAI 
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# List 10 fine-tuning jobs
client.fine_tuning.jobs.list()

 