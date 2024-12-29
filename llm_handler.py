from transformers import AutoTokenizer, AutoModelForCausalLM
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class LLMHandler:
    def __init__(self, model_name="mistralai/mistral-7b"):
        """
        Initialise le gestionnaire LLM.
        :param model_name: Nom du modèle Hugging Face à utiliser.
        """
        logging.info(f"Chargement du modèle {model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        logging.info(f"Modèle {model_name} chargé avec succès.")

    def generate_response(self, prompt: str) -> str:
        """
        Génère une réponse basée sur un prompt donné.
        :param prompt: Texte d'entrée pour le modèle.
        :return: Réponse générée par le modèle.
        """
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_length=150, num_return_sequences=1)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        logging.info(f"Réponse générée : {response}")
        return response
