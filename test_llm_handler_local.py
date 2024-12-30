from api.llm_handler import LLMHandler

if __name__ == "__main__":
    # Initialiser le gestionnaire avec un modèle causal et un dispositif CPU
    model_name = "EleutherAI/gpt-neo-2.7B"
    device = "cpu"
    model_type = "causal"  # Spécifie que le modèle est causal
    llm_handler = LLMHandler(model_name=model_name, device=device, model_type=model_type)

    # Prompt de test
    prompt = "Quel est le temps aujourd'hui ?"
    response = llm_handler.generate_response(prompt)

    # Afficher la réponse générée
    print(f"Prompt : {prompt}")
    print(f"Réponse : {response}")
