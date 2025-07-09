import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import call_function, available_functions

# Load environment variables
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not set.")
    sys.exit(1)

# Get user prompt and verbose flag
if len(sys.argv) < 2:
    print("Usage: python main.py 'your prompt' [--verbose]")
    sys.exit(1)

user_prompt = sys.argv[1]
verbose = "--verbose" in sys.argv

# Set model and system prompt
model_name = "gemini-2.0-flash-001"

system_prompt = """
You are a helpful AI coding agent.

Your job is to complete coding tasks by using available function calls. You MUST use the tools provided to gather information or take action — do not guess.

Available actions:
- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files
- Call functions

All paths should be relative. Use the tools step-by-step to solve the user's request, and only give a final response once the task is complete.
"""

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Create initial messages list
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
]

# Create tools and config
tools = [available_functions]
config = types.GenerateContentConfig(tools=tools, system_instruction=system_prompt)

# Run loop
MAX_ITERATIONS = 20
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

for iteration in range(MAX_ITERATIONS):
    print(f"\n--- Iteration {iteration + 1} ---")

    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=config,
    )

    candidate = response.candidates[0]
    messages.append(candidate.content)

    # Check if the model is making a function call
    if candidate.content.parts and candidate.content.parts[0].function_call:
        function_call = candidate.content.parts[0].function_call
        function_result = call_function(function_call, verbose=verbose)

        # Append tool result to messages
        messages.append(function_result)

        if verbose:
            print(f"-> {function_result.parts[0].function_response.response}")

        continue  #  Keep looping — model may need another function call

    # Otherwise, if it's a text response, assume we're done
    elif candidate.content.parts and candidate.content.parts[0].text:
        print("\nFinal response:\n")
        print(candidate.content.parts[0].text)
        break  #  Done — break out of the loop