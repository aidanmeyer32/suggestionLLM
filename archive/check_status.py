from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

job_id = 'ftjob-j7pbWSsJ1G0wyNBWLNCa6EFz'
job = client.fine_tuning.jobs.retrieve(job_id)

print(f"Status: {job.status}")
print(f"Error message: {job.error}")
print(f"Training file: {job.training_file}")

# Get detailed file information
file_info = client.files.retrieve(job.training_file)
print(f"\nFile details:")
print(f"File name: {file_info.filename}")
print(f"File purpose: {file_info.purpose}")
print(f"File status: {file_info.status}") 