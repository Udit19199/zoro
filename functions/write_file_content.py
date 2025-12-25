import os
from google.genai import types


def write_file(working_directory, file_path, content):
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_dir = os.path.abspath(working_directory)
    dir_path = os.path.dirname(abs_file_path)

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: {e}"


schema_write_file_content = types.FunctionDeclaration(
    name="write_file_content",
    description="Write the given contents to the specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write the contents to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content that has to be written to the specified file",
            ),
        },
    ),
)
