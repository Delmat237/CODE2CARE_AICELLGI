# sentiment/urls.py
from django.urls import path
from .views import home, predict_sentiment

urlpatterns = [
    path('', home),
    path('predict/', predict_sentiment, name='predict-sentiment'),
]
