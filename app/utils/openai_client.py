from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from root .env file
load_dotenv()

# Get API key from environment
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    print("WARNING: OPENAI_API_KEY not found in environment variables!")
    print("Please set OPENAI_API_KEY in your .env file or environment variables")
else:
    print(f"OpenAI API Key loaded: {api_key[:20]}..." if len(api_key) > 20 else "API key found but too short")

client = OpenAI(api_key=api_key)
