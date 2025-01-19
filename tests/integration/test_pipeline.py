from src.api.llm_handler import LLMHandler
from src.api.tiktok_live import TikTokLiveHandler
from src.wav2lip.Wav2LipHandler import Wav2LipHandler

def test_pipeline():
    llm_handler = LLMHandler(model_name="test-model")
    #tiktok_handler = TikTokLiveHandler(username="@test_user")
    wav2lip_handler = Wav2LipHandler(checkpoint_path="src/wav2lip/checkpoints/wav2lip.pth")

    # Simule un commentaire
    comment = {"user": "test_user", "comment": "Bonjour, test !"}
    prompt = f"Un utilisateur a dit : '{comment['comment']}'"
    response = llm_handler.generate_response(prompt)

    # Génère un fichier audio
    audio_path = "test_audio.wav"
    llm_handler.text_to_speech(response, output_path=audio_path)

    # Synchronise avec une vidéo
    video_output = wav2lip_handler.sync_lips("test_video.mp4", audio_path)
    assert video_output.endswith(".mp4")
