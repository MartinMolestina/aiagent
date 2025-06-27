import os

def write_file(working_directory, file_path, content):
    try:
        # convert to abs paths
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(file_path)

        # Prevent writing outside working dir
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Make sure parent dir exists
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)

        # Overwrite or write the file
        with open(abs_file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"