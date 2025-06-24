import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types



# Load environment variables from .env
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not set in environment.")
    sys.exit(1)

# Check for user input
if len(sys.argv) < 2:
    print("Usage: python script.py 'your prompt here'")
    sys.exit(1)


user_prompt = sys.argv[1]
model = "gemini-2.0-flash-001"

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

# Initialize the Gemini client
client = genai.Client(api_key=api_key)

# Generate the response
response = client.models.generate_content(model=model, contents=messages)

# Print input and response
print(f"Prompt:\n{contents}\n\nResponse:\n{response.text}\n")

# Print token usage
prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

print(f"Prompt tokens: {prompt_tokens}")
print(f"Response tokens: {response_tokens}")