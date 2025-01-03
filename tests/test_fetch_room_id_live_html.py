from todelete import FetchRoomIdLiveHTMLRoute  # Import de la classe modifiée

""""""
def test_valid_sigi_state():
    """
    Test de réussite avec un fichier HTML contenant une structure valide de SIGI_STATE.
    """
    # Charger le contenu HTML depuis le fichier live_html.html
    with open("ressources/live_html.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    # Appeler la méthode parse_room_id pour extraire le roomId
    room_id = FetchRoomIdLiveHTMLRoute.parse_room_id(html_content)

    # Vérifier que le roomId extrait correspond à l'attendu
    assert room_id == "7455736059944815366", "Le room ID extrait ne correspond pas à l'attendu."


