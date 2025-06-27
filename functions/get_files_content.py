import os

def get_file_content(working_directory, file_path):
    try:
        # Convert to absolute paths
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(file_path)

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