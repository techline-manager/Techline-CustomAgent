import openai
from dotenv import load_dotenv
import os

load_dotenv()  # load .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

# Example call
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message["content"])
