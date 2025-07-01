import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info



# Load environment variables from .env
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not set in environment.")
    sys.exit(1)

# Define system prompt for behavior
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


# Define schema for function calling by AI
available_functions = types.Tool(
    function_declarations=[schema_get_files_info]
)

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
response = client.models.generate_content(
    model=model,
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
    )
)


if response.candidates and response.candidates[0].content.parts:
    part = response.candidates[0].content.parts[0]

    if hasattr(part, "function_call"):
        print(f"Calling function: {part.function_call.name}({part.function_call.args})")
    else:
        print(part.text)
else:
    print("No response content received.")


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
