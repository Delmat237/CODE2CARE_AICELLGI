from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SentimentRequestSerializer
import torch
from transformers import XLMRobertaTokenizer
from django.http import JsonResponse

model_path = 'D:/Summer25FastCoding/Dev/HackCode/serengeti_full_model.pt'
model = torch.load(model_path, map_location=torch.device('cpu'), weights_only=False)
model.eval()
if not hasattr(model.config, '_output_attentions'):
    setattr(model.config, '_output_attentions', False)

tokenizer = XLMRobertaTokenizer.from_pretrained('xlm-roberta-base')

def home(request):
    return JsonResponse({"message": "Hello Bro, ici AICELL. Bienvenue sur l'API de prédiction de sentiments !"})

@api_view(['POST'])
def predict_sentiment(request):
    serializer = SentimentRequestSerializer(data=request.data)
    if serializer.is_valid():
        text = serializer.validated_data['text']
        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        outputs = model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=1).item()

        labels = {0: 'Négatif', 1: 'Neutre', 2: 'Positif'}
        label = labels.get(prediction, "Inconnu")

        return Response({'sentiment': prediction, 'label': label})

    return Response(serializer.errors, status=400)
