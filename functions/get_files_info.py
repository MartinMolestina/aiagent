import os
from google.genai import types


def get_files_info(working_directory, directory=None):
    # If no directory is passed, work on current directory
    target_dir = directory or working_directory

    # get absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_dir = os.path.abspath(target_dir)

    # check if target directory is outside the working directory
    if not abs_target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # Check if target is a directory 
    if not os.path.isdir(abs_target_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        entries = os.listdir(abs_target_dir)
        lines = []

        for entry in entries:
            full_path = os.path.join(abs_target_dir, entry)
            is_dir = os.path.isdir(full_path)

            try:
                size = os.path.getsize(full_path)
            except OSError:
                size = 0 # if file is unreadable

            lines. append(f"- {entry}: file_size={size}, bytes, is_dir={is_dir}")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {str(e)}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

