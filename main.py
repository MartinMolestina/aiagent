import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_files_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python import schema_run_python_file, run_python_file

# Load environment variables
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not set.")
    sys.exit(1)

# Check input args
if len(sys.argv) < 2:
    print("Usage: python main.py 'your prompt' [--verbose]")
    sys.exit(1)

user_prompt = sys.argv[1]
verbose = "--verbose" in sys.argv

# Setup model + system prompt
model_name = "gemini-2.0-flash-001"

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Tools (function declarations)
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Create content input
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
]

# Configure content generation
config = types.GenerateContentConfig(
    tools=[available_functions],
    system_instruction=system_prompt
)

# Call the model
response = client.models.generate_content(
    model=model_name,
    contents=messages,
    config=config,
)

# Handle responses
for candidate in response.candidates:
    for part in candidate.content.parts:
        if part.function_call:
            fn_name = part.function_call.name
            fn_args = part.function_call.args
            print(f"Calling function: {fn_name}({fn_args})")

            # Inject working directory
            working_directory = "calculator"

            try:
                if fn_name == "get_files_info":
                    result = get_files_info(working_directory, **fn_args)
                elif fn_name == "get_file_content":
                    result = get_file_content(working_directory, **fn_args)
                elif fn_name == "write_file":
                    result = write_file(working_directory, **fn_args)
                elif fn_name == "run_python_file":
                    result = run_python_file(working_directory, **fn_args)

                else:
                    result = f"Error: Unknown function '{fn_name}'"
            except Exception as e:
                result = f"Error: {e}"

            print(f"\nFunction result:\n{result}")
        elif part.text:
            print(f"\nResponse:\n{part.text}")
        else:
            print("Warning: part contains no function_call or text")


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
