from api.tiktok_live import TikTokLiveHandler

if __name__ == "__main__":
    username = "@magali.berdah"  # Remplacez par un utilisateur réel en live
    tiktok_handler = TikTokLiveHandler(username=username)

    try:
        tiktok_handler.start()
    except KeyboardInterrupt:
        logging.info("Arrêt du programme.")

        # Récupérer et afficher les commentaires
        new_comments = tiktok_handler.get_comments()
        logging.info(f"Commentaires non traités : {new_comments}")

        # Sauvegarder les commentaires restants
        tiktok_handler.save_comments_to_file()

