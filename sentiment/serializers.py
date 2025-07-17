# sentiment/serializers.py
from rest_framework import serializers

class SentimentRequestSerializer(serializers.Serializer):
    text = serializers.CharField()
