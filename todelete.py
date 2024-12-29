try:
    from TikTokLive.types.events import CommentEvent
    print("Importation réussie : CommentEvent est disponible.")
except ModuleNotFoundError as e:
    print(f"Erreur d'importation : {e}")
