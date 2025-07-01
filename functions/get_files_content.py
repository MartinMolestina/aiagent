import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of a file, truncated at 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to read, relative to the working directory."
            )
        }
    )
)


def get_file_content(working_directory, file_path):
    try:
        # Convert to absolute paths
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        # CHeck if path is working dir
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # File must exist and be a regular file
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read and truncate size
        with open(abs_file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if len(content) > 10000:
            truncated_msg = f'\n\n[...File "{file_path}" truncated at 10000 characters]'
            return content[:10000] + truncated_msg

        return content

    except Exception as e:
        return f"Error: {str(e)}"