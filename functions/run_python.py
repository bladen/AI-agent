import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)

    working_dir = os.path.abspath(working_directory)
    abs_file = os.path.abspath(full_path)

    if not abs_file.startswith(working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file):
        return f'Error: File "{file_path}" not found.'
    if not abs_file.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    

    try:  
        completed_process = subprocess.run(
            ["python", abs_file, *args],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=working_dir
        )

        output = []

        if completed_process.stdout.strip():
            output.append(f"STDOUT:\n{completed_process.stdout.strip()}")

        if completed_process.stderr.strip():
            output.append(f"STDERR:\n{completed_process.stderr.strip()}")

        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")

        if not output:
            return "No output produced."

        return "\n\n".join(output)

    except subprocess.TimeoutExpired:
        return "Error: Execution timed out after 30 seconds."
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the python file",
            ),
        },
    ),
)