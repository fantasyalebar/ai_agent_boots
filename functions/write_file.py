import os 
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
    
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.abspath(os.path.join(abs_working_dir, file_path))

        if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
    
        parent_dir = os.path.dirname(target_dir)
        os.makedirs(parent_dir, exist_ok=True)

        with open(target_dir, "w") as f:
            f.write(content)
            
        # 6. Retourner le message de succès
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
     
    except Exception as e:
        # 7. Retourner l'erreur si quelque chose a planté
        return f"Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="write the file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Le chemin du fichier à écrire"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Le contenu textuel à écrire dans le fichier"
            ),
        },
        required=["file_path","content"]
    )
)