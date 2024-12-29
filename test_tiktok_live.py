from api.tiktok_live import TikTokLiveHandler
from api.llm_handler import LLMHandler

if __name__ == "__main__":
    username = "@le_l_br"  # Remplacez par un utilisateur réel en live
    tiktok_handler = TikTokLiveHandler(username=username)
    llm_handler = LLMHandler(model_name="mistralai/mistral-7b")  # Modèle LLM

    try:
        tiktok_handler.start()
    except KeyboardInterrupt:
        logging.info("Arrêt du programme.")

        # Récupérer les commentaires non traités
        new_comments = tiktok_handler.get_comments()
        logging.info(f"Commentaires à traiter : {new_comments}")

        # Générer des réponses pour chaque commentaire
        for comment in new_comments:
            prompt = comment["comment"]
            response = llm_handler.generate_response(prompt)
            logging.info(f"Prompt : {prompt} | Réponse : {response}")

        # Sauvegarder les commentaires restants
        tiktok_handler.save_comments_to_file()
