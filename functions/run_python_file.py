import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_dir = os.path.abspath(working_directory)

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    command_list = ["python", abs_file_path] + args
    try:
        completed_process = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_dir,
        )
        stdout = completed_process.stdout
        stderr = completed_process.stderr
        returncode = completed_process.returncode

        lines = []
        if stdout:
            lines.append(f"STDOUT: {stdout}")
        if stderr:
            lines.append(f"STDERR: {stderr}")
        if returncode != 0:
            lines.append(f"Process exited with code {returncode}")

        if len(lines) == 0:
            return "No output produced"
        return "\n".join(lines)

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to get the contents of. ",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Additional Arguments to run the python file with. ",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A single argument to pass to the Python process",
                ),
            ),
        },
    ),
)
