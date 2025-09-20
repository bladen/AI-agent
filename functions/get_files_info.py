import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)

    working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(full_path)

    if not target_dir.startswith(working_dir):
        return (
            f"Result for '{target_dir}' directory:\n"
            f'  Error: Cannot list "{directory}" as it is outside the permitted working directory'
        )
    elif not os.path.isdir(target_dir):
        return (
            f"Result for '{target_dir}' directory:\n"
            f'  Error: "{directory}" is not a directory'
        )
    
    try:
        dir_list = os.listdir(target_dir)
        result_entries = [f"Result for '{full_path}' directory:"]
        for dir_list_item in dir_list:
            fpath = os.path.join(target_dir, dir_list_item)
            fsize = os.path.getsize(fpath)
            fdir = os.path.isfile(fpath)
            result = f"- {dir_list_item}: file_size={fsize}, is_dir={fdir}"
            result_entries.append(result)


        return "\n".join(result_entries)

    except Exception as e:
        return f"Error: {e}"
    

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
