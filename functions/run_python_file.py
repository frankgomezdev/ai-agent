import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a specific .py file that already exists in the working directory, optionally with CLI args.",
        "parameters": {
            "required": ["file_path"],
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File where Python code will be run. Must be a .py file",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "CLI arguments passed to the script.",
                },
            },
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        is_within_working_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not is_within_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)

        result = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)

        lines = []

        if result.returncode != 0:
            line = f"Process exited with code {result.returncode}"
            lines.append(line)

        if not result.stdout and not result.stderr:
            line = f"No output produced"
            lines.append(line)

        if result.stdout:
            line = f"STDOUT: {result.stdout}"
            lines.append(line)

        if result.stderr:    
            line = f"STDERR: {result.stderr}"
            lines.append(line)

        output = "\n".join(lines)
        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"