import os 
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, file_path))

        if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
        MAX_CHARS = 10000

        with open(target_dir, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):  # essaie de lire un caractère de plus
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        return content
    
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the content of a file in the working directory",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "file_path": types.Schema(
                type="STRING",
                description="The path to the file to read",
            ),
        },
        required=["file_path"],
    ),
)