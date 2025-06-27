import os

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


def get_file_content(working_directory, file_path):
    try:
        # Convert to absolute paths
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(file_path)

        # CHeck if path is working dir
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: cannot read"{file_path}"as it is outside the permitted working directory'

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