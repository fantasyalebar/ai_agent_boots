import os
from google import genai
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        # On commence par la validation
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Sécurité
        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # Est-ce un dossier ?
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # On liste les fichiers
        lignes = []
        for nom in os.listdir(target_dir):
            chemin_complet = os.path.join(target_dir, nom)
            taille = os.path.getsize(chemin_complet)
            est_dossier = os.path.isdir(chemin_complet)
            lignes.append(f"- {nom}: file_size={taille} bytes, is_dir={est_dossier}")
        
        return "\n".join(lignes)

    except Exception as e:
        # En cas de pépin imprévu (permission, fichier supprimé, etc.)
        return f"Error: {e}"
        
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["directory"],
    ),
)





