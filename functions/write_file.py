import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)

    working_dir = os.path.abspath(working_directory)
    abs_file = os.path.abspath(full_path)

    if not abs_file.startswith(working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file):
        try:
            os.makedirs(os.path.dirname(abs_file), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
        
    if os.path.exists(abs_file) and os.path.isdir(abs_file):
        return f'Error: "{file_path}" is a directory, not a file'
    
    try:  
        with open(abs_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'    
    except Exception as e:
        return f"Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Contents to write",
            ),
        },
        required=["file_path", "content"],
    ),
)
