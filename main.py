import os
import argparse
from prompts import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions, call_function


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # Vérification de la clé
    if not api_key:
        raise RuntimeError("votre message ici")

    client = genai.Client(api_key=api_key, http_options={'api_version': 'v1beta'})
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for i in range(20):
        # Appel au modèle
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0
            )
        )

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        # On regarde ce que l'IA a décidé de faire
        if response.function_calls:
            function_results = []
            # BOUCLE : On exécute toutes les fonctions demandées
            for function_call in response.function_calls:
                # On appelle l'outil
                function_call_result = call_function(function_call, args.verbose)

                # On extrait le résultat (le "part")
                part = function_call_result.parts[0]

                # On l'ajoute à notre liste temporaire
                function_results.append(part)

                if args.verbose:
                    print(f"-> {part.function_response.response}")

            # APRÈS LA BOUCLE : On ajoute TOUS les résultats à l'historique
            messages.append(types.Content(role="user", parts=function_results))
        else:
            # Si elle veut juste parler, on affiche son texte
            print(response.text)
            break

        # Métadonnées à chaque tour de boucle
        if args.verbose:
            if response.usage_metadata is None:
                raise RuntimeError("Gemini API is missing")
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        # Cette partie s'exécute si on arrive à i = 19 sans 'break'
        print("Max iterations reached without a final response.")
        import sys
        sys.exit(1)


if __name__ == "__main__":
    main()
