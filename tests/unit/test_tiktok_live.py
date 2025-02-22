import logging
import asyncio
import random
import os
from queue import Queue
from threading import Thread

from api.tiktok_live import TikTokLiveHandler

from api.llm_handler import LLMHandler
from wav2Lip.Wav2LipHandler import Wav2LipHandler

# Chemins des dossiers
BASE_DIR = "../../interactive_ia"
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
VIDEO_DIR = os.path.join(BASE_DIR, "results")
BASE_VIDEO = os.path.join(BASE_DIR, "asmr_girl.mp4")

# Configuration des logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")



def test_tiktok_live(mock_tiktok_live_api):
    """
    Teste la réception de commentaires avec TikTok Live simulé.
    """
    from api.tiktok_live import TikTokLiveHandler
    handler = TikTokLiveHandler(username="@test_user")
    handler.start()
    comments = handler.get_comments()
    assert len(comments) == 1
    assert comments[0]["comment"] == "Commentaire simulé"


def test_comment_listeners(mock_tiktok_live_api):
    """
    Teste que les listeners de commentaires sont appelés correctement.
    """
    from src.api.tiktok_live import TikTokLiveHandler

    # Initialiser le gestionnaire
    handler = TikTokLiveHandler(username="@test_user")
    mock_comment = {"user": "test_user", "comment": "Test listener"}

    # Ajouter un listener
    received_comments = []
    handler.add_comment_listener(received_comments.append)

    # Simuler un commentaire
    handler.comments = [mock_comment]

    # Notifier les listeners
    for listener in handler.comment_listeners:
        listener(mock_comment)

    # Vérifier que le listener a bien reçu le commentaire
    assert len(received_comments) == 1
    assert received_comments[0] == mock_comment

"""
async def process_audio_response(queue: Queue, llm_handler: LLMHandler, wav2lip_handler: Wav2LipHandler):
"""
#Traite les commentaires pour générer des fichiers audio et des vidéos synchronisées.
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

            # Générer le prompt et la réponse
            prompt = format_prompt(comment["comment"])
            logging.info(f"Envoi du prompt à OpenAI : {prompt}")
            response = "".join(llm_handler.generate_response_stream(prompt))
            logging.info(f"Réponse générée : {response}")

            # Générer un fichier audio pour la réponse
            audio_filename = f"response_{hash(prompt)}.wav"
            audio_path = os.path.join(AUDIO_DIR, audio_filename)
            llm_handler.text_to_speech(response, output_path=audio_path)  # Ajoutez text_to_speech à LLMHandler
            logging.info(f"Audio généré et sauvegardé : {audio_path}")

            # Synchroniser l'audio avec la vidéo
            video_filename = f"video_{hash(prompt)}.mp4"
            video_output_path = os.path.join(VIDEO_DIR, video_filename)
            wav2lip_handler.sync_lips(BASE_VIDEO, audio_path, video_output_path)
            logging.info(f"Vidéo générée : {video_output_path}")
        else:
            await asyncio.sleep(1)  # Attendre avant de vérifier à nouveau la file
"""
if __name__ == "__main__":
    # Vérifiez et créez les dossiers nécessaires
    os.makedirs(AUDIO_DIR, exist_ok=True)
    os.makedirs(VIDEO_DIR, exist_ok=True)

    username = "@bayanistka55"  # Remplacez par un utilisateur réel en live
    model_name = "gpt-4o-mini-2024-07-18"

    # Initialisation des gestionnaires
    tiktok_handler = TikTokLiveHandler(username=username)
    llm_handler = LLMHandler(model_name=model_name)
    wav2lip_handler = Wav2LipHandler(checkpoint_path="src/wav2Lip/checkpoints/wav2lip.pth")

    # Création d'une file d'attente pour les commentaires
    comment_queue = Queue()

    # Thread pour écouter les commentaires
    listener_thread = Thread(target=listen_for_comments, args=(tiktok_handler, comment_queue))
    listener_thread.start()

    # Lancer la boucle principale pour traiter les commentaires et générer les vidéos
    asyncio.run(process_audio_response(comment_queue, llm_handler, wav2lip_handler))
