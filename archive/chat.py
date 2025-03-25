# This script will allow the user to chat with GPT 4o from the command line.

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load the OpenAI API key from the environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def chat_with_gpt(prompt):
    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Give insight about the emergency alert system ",
                },
                {"role": "user", "content": prompt},
            ],
            model= "ft:gpt-4o-mini-2024-07-18:university-of-mary-washington::AaxgQQAe",
            temperature=.2,
            max_completion_tokens=300 
        )
        return completion
    except Exception as e:
        print(f"Failed to get response: {e}")
        return "Error in processing your request."


if __name__ == "__main__":
    print("Welcome to the GPT-4 chat interface. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        completion = chat_with_gpt(user_input)
        print("Assistant: " + completion.choices[0].message.content)
