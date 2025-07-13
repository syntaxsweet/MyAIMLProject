# core/emotion.py

from transformers import pipeline

emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)

def detect_emotion(text):
    results = emotion_model(text)[0]
    emotion = max(results, key=lambda x: x['score'])
    return emotion['label'], emotion['score']
