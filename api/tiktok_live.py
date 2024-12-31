from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent
import asyncio
import logging

# Configuration des logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class TikTokLiveHandler:
    def __init__(self, username: str):
        """
        Initialise le gestionnaire TikTokLive.
        :param username: Nom d'utilisateur TikTok pour le live (public).
        """
        self.username = username
        self.client = TikTokLiveClient(unique_id=username)
        self.comments = []  # Stocker les commentaires reçus

    async def on_connect(self, event: ConnectEvent):
        """
        Déclenché lors de la connexion au live.
        :param event: Contient des informations sur la connexion.
        """
        logging.info(f"Connecté au live de @{event.unique_id} (Room ID: {self.client.room_id})")

    async def on_comment(self, event: CommentEvent):
        """
        Déclenché lorsqu'un commentaire est reçu.
        :param event: Contient des informations sur le commentaire.
        """
        comment_data = {
            "user": event.user.nickname,
            "comment": event.comment
        }
        self.comments.append(comment_data)  # Stocker le commentaire
        logging.info(f"Commentaire reçu - {event.user.nickname}: {event.comment}")

    def start(self):
        """
        Démarre l'écoute des événements du live TikTok.
        """
        # Ajouter des écouteurs pour les événements
        self.client.add_listener(ConnectEvent, self.on_connect)
        self.client.add_listener(CommentEvent, self.on_comment)

        try:
            # Démarrer le client
            logging.info(f"Connexion au live TikTok pour l'utilisateur : {self.username}")
            asyncio.run(self.run_client())
        except Exception as e:
            logging.error(f"Erreur lors de la connexion au live : {e}")

    async def run_client(self):
        """
        Méthode asynchrone pour exécuter le client.
        """
        try:
            await self.client.start()
        except asyncio.CancelledError:
            logging.info("Client TikTokLive arrêté proprement.")
        finally:
            await self.client.disconnect()  # Assurez-vous que la connexion est fermée

    def get_comments(self):
        """
        Récupère les commentaires non traités.
        Retourne une liste de nouveaux commentaires et les marque comme traités.
        """
        if not hasattr(self, "processed_comments"):
            self.processed_comments = set()

        logging.info(f"Total des commentaires reçus : {len(self.comments)}")
        new_comments = [
            comment for comment in self.comments
            if comment["comment"] not in self.processed_comments
        ]

        # Marque les commentaires comme traités
        for comment in new_comments:
            self.processed_comments.add(comment["comment"])

        logging.info(f"Récupération de {len(new_comments)} nouveaux commentaires.")
        return new_comments

    def save_comments_to_file(self, filename="comments.json"):
        """
        Sauvegarde les commentaires dans un fichier JSON.
        :param filename: Nom du fichier pour stocker les commentaires.
        """
        try:
            with open(filename, "w") as f:
                json.dump(self.comments, f, indent=4)
            logging.info(f"Commentaires sauvegardés dans {filename}")
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde des commentaires : {e}")


    def save_responses(self, responses, filename="responses.json"):
        """
        Sauvegarde les réponses générées dans un fichier JSON.
        :param responses: Liste de réponses à sauvegarder.
        :param filename: Nom du fichier pour stocker les réponses.
        """
        try:
            with open(filename, "w") as f:
                json.dump(responses, f, indent=4, ensure_ascii=False)
            logging.info(f"Réponses sauvegardées dans {filename}")
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde des réponses : {e}")