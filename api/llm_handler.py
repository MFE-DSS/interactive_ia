import openai
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class LLMHandler:
    def __init__(self, model_name="gpt-4"):
        """
        Initialise le gestionnaire LLM basé sur l'API OpenAI.
        :param model_name: Nom du modèle OpenAI à utiliser (e.g., "gpt-4" ou "gpt-3.5-turbo").
        """
        self.model_name = model_name
        logging.info(f"LLMHandler initialisé avec le modèle {self.model_name}.")

    def generate_response(self, prompt: str) -> str:
        """
        Génère une réponse basée sur un prompt donné en utilisant l'API OpenAI.
        :param prompt: Texte d'entrée pour le modèle.
        :return: Réponse générée par le modèle.
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "Tu es un assistant amical et aidant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150,
                top_p=0.9,
            )
            # Retourne la réponse générée par le modèle
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logging.error(f"Erreur lors de la génération de la réponse : {e}")
            return "Je suis désolé, je ne peux pas répondre pour le moment."
