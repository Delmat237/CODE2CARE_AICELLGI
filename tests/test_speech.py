from google.cloud import speech
import os

def test_speech_client():
    # Initialiser le client
    client = speech.SpeechClient()
    print("SpeechClient initialisé avec succès !")

    # Exemple de fichier audio (remplacez par un chemin valide)
    audio_file = "/home/delmat/Hackathon_DGH/Track1/backend/tests/sample.wav"

    with open(audio_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="fr-FR",
    )

    # Effectuer la transcription
    response = client.recognize(config=config, audio=audio)

    # Afficher les résultats
    for result in response.results:
        print("Transcription : {}".format(result.alternatives[0].transcript))

if __name__ == "__main__":
    test_speech_client()