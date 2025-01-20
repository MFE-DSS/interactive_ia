import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))


import pytest

@pytest.fixture
def mock_openai_api(monkeypatch):
    """
    Mock les appels API OpenAI pour les tests.
    """
    def mock_generate_response(self, prompt: str):
        return "Réponse simulée"

    def mock_generate_response_stream(self, prompt: str):
        yield "Réponse simulée en streaming"

    # Remplacer les méthodes dans LLMHandler
    monkeypatch.setattr("src.api.llm_handler.LLMHandler.generate_response", mock_generate_response)
    monkeypatch.setattr("src.api.llm_handler.LLMHandler.generate_response_stream", mock_generate_response_stream)

@pytest.fixture
def mock_tiktok_live_api(monkeypatch):
    """
    Mock les appels TikTok Live pour les tests.
    """
    def mock_start(self):
        self.comments = [{"user": "test_user", "comment": "Commentaire simulé"}]

    def mock_get_comments(self):
        return self.comments

    # Remplacer les méthodes dans TikTokLiveHandler
    monkeypatch.setattr("src.api.tiktok_live.TikTokLiveHandler.start", mock_start)
    monkeypatch.setattr("src.api.tiktok_live.TikTokLiveHandler.get_comments", mock_get_comments)
