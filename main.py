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

# Check for input args
if len(sys.argv) < 2:
    print("Usage: python script.py 'your prompt here' [--verbose]")
    sys.exit(1)

# Check if --verbose flag is present
verbose = "--verbose" in sys.argv

# Join all arguments that are NOT the --verbose flag
user_prompt = " ".join(arg for arg in sys.argv[1:] if arg != "--verbose")

model = "gemini-2.0-flash-001"

# Prepare message for Gemini API
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

# Initialize the Gemini client
client = genai.Client(api_key=api_key)

# Generate the response
response = client.models.generate_content(model=model, contents=messages)

# Only print verbose info if --verbose was passed
if verbose:
    print(f"User prompt: {user_prompt}\n")
    print(f"\nResponse:\n{response.text}\n")
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")

else:
    print(f"\nResponse:\n{response.text}\n")
