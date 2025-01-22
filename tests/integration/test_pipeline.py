import os
import pytest


def test_project_structure():
    """
    Vérifie que les fichiers et dossiers clés existent.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    required_files = [
        os.path.join(base_dir, "README.md"),
        os.path.join(base_dir, "requirements.txt"),
        os.path.join(base_dir, "src", "api", "llm_handler.py"),
        os.path.join(base_dir, "src", "api", "tiktok_live.py"),
        os.path.join(base_dir, "src", "wav2Lip"),
        os.path.join(base_dir, "tests", "unit", "test_llm_handler.py"),
        os.path.join(base_dir, "tests", "unit", "test_tiktok_live.py"),
        os.path.join(base_dir, "tests", "integration", "test_pipeline.py"),
    ]

    for file_path in required_files:
        assert os.path.exists(file_path), f"Fichier ou dossier manquant : {file_path}"


def test_imports():
    """
    Vérifie que les modules principaux peuvent être importés sans erreur.
    """
    try:
        from api.llm_handler import LLMHandler
        from api.tiktok_live import TikTokLiveHandler
        from wav2Lip.Wav2LipHandler import Wav2LipHandler
    except ImportError as e:
        pytest.fail(f"Échec de l'importation : {e}")


def test_pipeline(mock_openai_api, mock_tiktok_live_api):
    """
    Teste le pipeline complet avec des mocks pour OpenAI et TikTok Live.
    """
    from api.llm_handler import LLMHandler
    from api.tiktok_live import TikTokLiveHandler

    # Initialiser les gestionnaires avec des mocks
    llm_handler = LLMHandler(model_name="test-model")
    tiktok_handler = TikTokLiveHandler(username="@test_user")

    # Simuler un commentaire
    tiktok_handler.start()
    comments = tiktok_handler.get_comments()
    assert len(comments) == 1
    assert comments[0]["comment"] == "Commentaire simulé"

    # Simuler une réponse avec le mock
    prompt = f"Un utilisateur a dit : '{comments[0]['comment']}'"
    response_stream = list(llm_handler.generate_response_stream(prompt))

    # Vérifier la réponse simulée
    assert response_stream == ["Réponse simulée en streaming"]
