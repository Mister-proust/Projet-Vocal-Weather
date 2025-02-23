from Scripts.speech_recognition import key, recognize_from_microphone
import os

# Récupère le chemin du répertoire courant du script
current_dir = os.path.dirname(__file__)
audio_file = os.path.join(current_dir, "..", "data", "test.wav")


def test_speech () :
    result = recognize_from_microphone()
    expected = "Bonjour, quelle météo fera-t-il à Saint-Paterne Racan jeudi prochain\xa0?"
    assert result == expected


