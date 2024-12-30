import os
import openai

# Charger la clé API depuis l'environnement
openai.api_key = os.getenv("OPENAI_API_KEY")
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class LLMHandler:
    def __init__(self, api_key=None, model_name="gpt-4"):
        """
        Initialise le gestionnaire LLM basé sur l'API OpenAI.
        :param api_key: Clé API OpenAI.
        :param model_name: Nom du modèle OpenAI à utiliser (e.g., "gpt-4" ou "gpt-3.5-turbo").
        """
        self.api_key = api_key or "INSERT_YOUR_API_KEY_HERE"
        self.model_name = model_name
        openai.api_key = self.api_key
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
                    {"role": "system", "content": "Tu es un assistant qui répond aux questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150,
                top_p=0.9,
            )
            message = response["choices"][0]["message"]["content"].strip()
            logging.info(f"Réponse générée : {message}")
            return message
        except Exception as e:
            logging.error(f"Erreur lors de la génération de la réponse : {e}")
            return "Je suis désolé, je ne peux pas répondre pour le moment."
