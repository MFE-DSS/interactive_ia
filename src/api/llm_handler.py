from openai import OpenAI
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class LLMHandler:
    def __init__(self, model_name="gpt-4o-mini-2024-07-18", api_key=None):
        """
        Initialise le gestionnaire LLM basé sur l'API OpenAI.
        :param model_name: Nom du modèle OpenAI à utiliser.
        :param api_key: Clé API OpenAI (optionnel si configurée dans l'environnement).
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("La clé API OpenAI doit être définie via api_key ou OPENAI_API_KEY.")

        # Initialiser le client OpenAI
        self.client = OpenAI(api_key=self.api_key)
        logging.info(f"LLMHandler initialisé avec le modèle {self.model_name}.")


    def generate_response_stream(self, prompt: str):
        """
        Génère une réponse en streaming pour un prompt donné.
        :param prompt: Texte d'entrée pour le modèle.
        :yield: Morceaux de réponse générés par le modèle.
        """
        try:
            stream = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "developer", "content": "Tu es un assistant amical et aidant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150,
                top_p=0.9,
                stream=True,
            )
            for chunk in stream:
                yield chunk.choices[0].delta.content or ""
        except Exception as e:
            logging.error(f"Erreur lors de la génération de la réponse en streaming : {e}")

    def store_response(self, prompt: str, response: str):
        """
        Stocke un prompt et une réponse dans un fichier JSON.
        :param prompt: Le prompt utilisé.
        :param response: La réponse générée.
        """
        data = {"prompt": prompt, "response": response}

        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, "r", encoding="utf-8") as file:
                    responses = json.load(file)
            else:
                responses = []

            responses.append(data)

            with open(self.storage_path, "w", encoding="utf-8") as file:
                json.dump(responses, file, ensure_ascii=False, indent=4)

            logging.info("Réponse stockée avec succès.")
        except Exception as e:
            logging.error(f"Erreur lors du stockage de la réponse : {e}")


