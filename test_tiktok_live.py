import logging
import asyncio
import random
from queue import Queue
from threading import Thread
from api.tiktok_live import TikTokLiveHandler
from api.llm_handler import LLMHandler

def format_prompt(comment: str) -> str:
    """
    Formate le prompt pour fournir un contexte au modèle.
    """
    return (
        f"Un utilisateur a laissé le commentaire suivant sur un live TikTok : '{comment}'. "
        "Réponds de manière aimable et concise en tenant compte du contexte d'un live TikTok."
    )

def listen_for_comments(handler: TikTokLiveHandler, queue: Queue):
    """
    Écoute les commentaires en continu et les ajoute dans une file d'attente.
    """
    def on_new_comment(comment):
        queue.put(comment)
        logging.info(f"Nouveau commentaire ajouté à la file d'attente : {comment}")

    handler.add_comment_listener(on_new_comment)
    handler.start()

async def process_comments(queue: Queue, llm_handler: LLMHandler):
    """
    Traite les commentaires dans la file d'attente et génère des réponses.
    """
    while True:
        if not queue.empty():
            comment = queue.get()

            # Filtrer les commentaires (e.g., plus de 4 mots)
            if len(comment["comment"].split()) <= 4:
                continue

            # Simuler une réponse aléatoire à certains commentaires
            if random.random() > 0.5:
                continue

            prompt = format_prompt(comment["comment"])
            logging.info(f"Envoi du prompt à OpenAI : {prompt}")

            # Génération de la réponse en streaming
            response_chunks = []
            for chunk in llm_handler.generate_response_stream(prompt):  # Utilisation de for
                response_chunks.append(chunk)
                print(chunk, end="")  # Afficher en temps réel

            response = "".join(response_chunks)
            logging.info(f"Réponse générée : {response}")

            # Stocker la réponse
            llm_handler.store_response(prompt, response)
        else:
            await asyncio.sleep(1)  # Attendre avant de vérifier à nouveau la file


if __name__ == "__main__":
    username = "@sofia_asmrtist"  # Remplacez par un utilisateur réel en live
    model_name = "gpt-4o-mini-2024-07-18"

    # Initialisation des gestionnaires
    tiktok_handler = TikTokLiveHandler(username=username)
    llm_handler = LLMHandler(model_name=model_name)

    # Création d'une file d'attente pour les commentaires
    comment_queue = Queue()

    # Thread pour écouter les commentaires
    listener_thread = Thread(target=listen_for_comments, args=(tiktok_handler, comment_queue))
    listener_thread.start()

    # Lancer la boucle principale pour traiter les commentaires
    asyncio.run(process_comments(comment_queue, llm_handler))
