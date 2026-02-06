from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from root .env file
load_dotenv()

client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY"), 
)

print(f"OpenAI API Key loaded: {client.api_key[:20]}..." if client.api_key else "No API key found")
