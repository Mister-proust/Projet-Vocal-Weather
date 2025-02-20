from Scripts.speech_recognition import key, recognize_from_microphone


def test_speech () :
    result = recognize_from_microphone()
    expected = "Que voulez vous savoir à propos de la météo ? Ce que vous avez demandé: Bonjour, quelle météo fera-t-il à Saint-Paterne Racan jeudi prochain ?"
    assert result == expected
