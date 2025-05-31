from openai import OpenAI
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv(openai_api_key))

# Create fine-tuning job
response = client.fine_tuning.jobs.create(
    training_file= "file-WCnexBcwcCd4B2dMchxM5a",
    model="gpt-4o-2024-08-06"
)

print(f"Fine-tuning job created: {response}")

# Track the job's progress
job_id = response.id

while True:
    job = client.fine_tuning.jobs.retrieve(job_id)
    print(f"Status: {job.status}")
    
    if job.status in ['succeeded', 'failed']:
        print(f"Final status: {job.status}")
        if job.fine_tuned_model:
            print(f"Fine-tuned model ID: {job.fine_tuned_model}")
        break
        
    # Check status every 60 seconds
    time.sleep(60)
