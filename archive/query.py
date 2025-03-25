# This script will allow the user to query the Chroma vector database. 

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Initialize the OpenAI API Key
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API Key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OpenAI API Key not found in environment variables.")

os.environ["OPENAI_API_KEY"] = openai_api_key

# Load the vector database
db_directory = "chroma_db"
vector_db = Chroma(persist_directory=db_directory, embedding_function=OpenAIEmbeddings())

def query_vector_db(query, top_k=3):
    """
    Query the vector database and return the top k related results.

    Args:
        query (str): The query string.
        top_k (int): The number of top related results to return.

    Returns:
        list: A list of the top k related results.
    """
    results = vector_db.similarity_search(query, k=top_k)
    return results

if __name__ == "__main__":
    query = "What are emergency alert system regulations?" 
    top_results = query_vector_db(query, top_k=3)
    
    for i, result in enumerate(top_results, 1):
        print(f"Result {i}: {result.page_content}")

