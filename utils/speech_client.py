from google.cloud import speech
import os

def get_speech_client():
    return speech.SpeechClient()

