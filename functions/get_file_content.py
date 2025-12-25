import os
from google.genai import types
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    abs_target = os.path.abspath(full_path)
    abs_working = os.path.abspath(working_directory)
    if not abs_target.startswith(abs_working):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_target):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_target, "r") as f:
            content = f.read(MAX_CHARS + 1)
            if len(content) > 10000:
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
            return content

    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get contents of the specified file truncated to 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to get the contents of. ",
            )
        },
    ),
)
