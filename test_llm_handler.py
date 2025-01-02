from api.llm_handler import LLMHandler
import logging
import os

# Récupérer la clé API
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("La clé API OpenAI n'est pas définie dans l'environnement.")

if __name__ == "__main__":
    # Initialiser le gestionnaire avec le modèle GPT-4
    llm_handler = LLMHandler(model_name="gpt-4o-mini-2024-07-18", api_key=api_key)

    # Prompt de test
    prompt = "Écris un haïku sur la programmation."
    logging.info(f"Renvoie une réponse simple et écourtée : {prompt}")

    # Test de la réponse simple
    response = llm_handler.generate_response(prompt)
    print(f"Réponse simple : {response}")

    # Test de la réponse en streaming
    print("Réponse en streaming : ", end="")
    for chunk in llm_handler.generate_response_stream(prompt):
        print(chunk, end="")
    print()
