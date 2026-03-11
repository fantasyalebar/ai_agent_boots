import os
import subprocess
from google.genai import types
def run_python_file(working_directory, file_path, args=None):
    try:

        abs_working_directory = os.path.abspath(working_directory)
        target_dir = os.path.abspath(os.path.join(abs_working_directory, file_path))

        if os.path.commonpath([abs_working_directory, target_dir]) != abs_working_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not target_dir.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python",target_dir]

        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=abs_working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )

        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        # Si les deux sont vides...
        if not result.stdout and not result.stderr:
            output.append("No output produced")

        # Sinon, on les ajoute s'ils existent...
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        # Étape 8 suite...
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        # Étape 9
        return "\n".join(output)

# Étap
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="run the python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Le chemin du fichier à écrire"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Arguments optionnels a passer au script pyhton"
            ),
        },
        required=["file_path"]
    )
)