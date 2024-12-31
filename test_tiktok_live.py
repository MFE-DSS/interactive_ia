from api.tiktok_live import TikTokLiveHandler
from api.llm_handler import LLMHandler
import logging

def format_prompt(comment: str) -> str:
    """
    Formate le prompt pour fournir un contexte au modèle.
    :param comment: Commentaire TikTok.
    :return: Prompt formaté.
    """
    return (
        f"Un utilisateur a laissé le commentaire suivant sur un live TikTok : '{comment}'. "
        "Réponds de manière aimable et concise en tenant compte du contexte d'un live TikTok."
    )

if __name__ == "__main__":
    username = "@subtiletvous_"  # Remplacez par un utilisateur réel en live
    model_name = "gpt-4"  # Modèle OpenAI

    # Initialisation des gestionnaires
    tiktok_handler = TikTokLiveHandler(username=username)
    llm_handler = LLMHandler(model_name=model_name)

    try:
        # Démarrage de l'écoute des commentaires
        tiktok_handler.start()
    except KeyboardInterrupt:
        logging.info("Arrêt du programme.")

        # Étape 1 : Récupérer les commentaires non traités
        new_comments = tiktok_handler.get_comments()
        logging.info(f"Commentaires à traiter : {new_comments}")

        # Étape 2 : Générer des réponses pour chaque commentaire
        responses = []
        for comment in new_comments:
            prompt = format_prompt(comment["comment"])
            response = llm_handler.generate_response(prompt)
            responses.append({"prompt": comment["comment"], "response": response})
            logging.info(f"Prompt : {prompt} | Réponse : {response}")

        # Étape 3 : Sauvegarder les réponses
        tiktok_handler.save_responses(responses)
        logging.info("Les réponses ont été sauvegardées.")
