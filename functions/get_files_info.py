import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        is_within_working_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not is_within_working_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        dir_contents = os.listdir(target_dir)

        lines = []
        for item in dir_contents:
            full_path = os.path.join(target_dir, item)
            is_item_dir = os.path.isdir(full_path)
            item_size = os.path.getsize(full_path)
            line = f'- {item}: file_size={item_size} bytes, is_dir={is_item_dir}'
            lines.append(line)

        result = "\n".join(lines)
        return result

        # return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        return f'Error: {str(e)}'

    