import os

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("La clé API n'est pas définie dans l'environnement.")
    exit(1)

print(f"Clé API récupérée : {api_key}")
