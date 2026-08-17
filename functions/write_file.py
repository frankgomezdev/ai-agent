import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write and overwrite files, within a strict limit.",
        "parameters": {
            "type": "object",
            "required:": ["file_path", "content"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File where content will be written or overwritten. File will be created if it doesn't exist.",
                },
                "content": {
                    "type": "string",
                    "description": "Content that will be written to file.",
                },
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        is_within_working_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not is_within_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
            return f'Error: {str(e)}'
