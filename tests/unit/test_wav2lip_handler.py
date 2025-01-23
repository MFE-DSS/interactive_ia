from wav2Lip.Wav2LipHandler import Wav2LipHandler

# Initialiser Wav2LipHandler
handler = Wav2LipHandler(checkpoint_path="wav2Lip/checkpoints/wav2lip.pth")

# Fichiers pour le test
video_path = "../ressources/video/asmr_girl.mp4"  # Vidéo d'entrée
audio_path = "response_audio.wav"  # Audio généré
output_path = "results/output.mp4"  # Vidéo de sortie

try:
    # Synchronisation des lèvres
    result_path = handler.sync_lips(video_path, audio_path, output_path)
    print(f"Vidéo générée avec succès : {result_path}")
except Exception as e:
    print(f"Erreur lors du test : {e}")
