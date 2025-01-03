import re
import json
from json import JSONDecodeError

from TikTokLive.client.web.routes.fetch_room_id_live_html import FailedParseRoomIdError
from httpx import Response
from typing import Optional

from TikTokLive.client.errors import UserOfflineError, UserNotFoundError
from TikTokLive.client.web.web_base import ClientRoute
from TikTokLive.client.web.web_settings import WebDefaults


class FetchRoomIdLiveHTMLRoute(ClientRoute):
    """
    Route to retrieve the room ID for a user.
    """

    SIGI_PATTERN: re.Pattern = re.compile(
        r"""<script id="SIGI_STATE" type="application/json">(.*?)</script>"""
    )

    async def __call__(self, unique_id: str) -> str:
        """
        Fetch the Room ID for a given unique_id from the page HTML.

        :param unique_id: The user's username
        :return: The room ID string
        """
        # Retrieve the livestream HTML
        response: Response = await self._web.get(
            url=WebDefaults.tiktok_app_url + f"/@{unique_id}/live",
            base_params=False
        )

        # Parse and return the room ID
        return self.parse_room_id(response.text)

    @classmethod
    def parse_room_id(cls, html: str) -> str:
        """
        Parse le room ID depuis le HTML.

        :param html: Contenu HTML de la page
        :return: Le room ID sous forme de chaîne
        :raises ValueError: En cas d'échec d'extraction ou d'absence de données
        """
        # Extraire le contenu JSON depuis la balise <script>
        match: Optional[re.Match[str]] = cls.SIGI_PATTERN.search(html)
        if not match:
            raise ValueError("La balise <script id='SIGI_STATE'> n'a pas été trouvée.")

        try:
            sigi_state: dict = json.loads(match.group(1))
        except json.JSONDecodeError as e:
            raise ValueError(f"Erreur de parsing JSON dans SIGI_STATE : {e}")

        # Naviguer dans la structure JSON pour trouver le room ID
        live_room_info = sigi_state.get("LiveRoom", {}).get("liveRoomUserInfo", {}).get("user", {})
        room_id = live_room_info.get("roomId")

        if not room_id:
            raise ValueError("Le roomId est introuvable dans les données JSON extraites.")

        return room_id

