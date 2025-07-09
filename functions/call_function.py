# functions/call_function.py

import os
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_files_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

working_directory = "."

FUNCTION_MAP = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args or {}

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    # Add working directory to arguments
    function_args["working_directory"] = working_directory

    if function_name not in FUNCTION_MAP:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    try:
        result = FUNCTION_MAP[function_name](**function_args)
    except Exception as e:
        result = f"Error: {str(e)}"

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )
