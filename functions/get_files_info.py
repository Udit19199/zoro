import os


def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        abs_target = os.path.abspath(full_path)
        abs_working = os.path.abspath(working_directory)
        if not abs_target.startswith(abs_working):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        contents = os.listdir(full_path)
        lines = []

        for name in contents:
            item_path = os.path.join(full_path, name)
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            line = f"- {name}: file_size={size} bytes, is_dir={is_dir}"
            lines.append(line)

        output = "\n".join(lines)
        return output
    except Exception as e:
        return f"Error: {e}"
