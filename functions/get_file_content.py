import os
from google.genai import types
from config import *

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)

    working_dir = os.path.abspath(working_directory)
    abs_file = os.path.abspath(full_path)

    if not abs_file.startswith(working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif os.path.isdir(abs_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    

    try:
        with open(abs_file, "r") as f:
            file_content = f.read(CHAR_LIMIT)
            if os.path.getsize(abs_file) > CHAR_LIMIT:
                file_content += (
                f'[...File "{file_path}" truncated at 10000 characters]'
                )
            return file_content
    except Exception as e:
        return f"Error: {e}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the contents of the file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file",
            ),
        },
    ),
)