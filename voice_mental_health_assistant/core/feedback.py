# core/feedback.py

import openai
import os
from dotenv import load_dotenv

# 🔐 Load API key securely from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_feedback(emotion):
    prompt = f"""
You are a compassionate mental health assistant. A user has shared a voice message and their emotion is: **{emotion}**.

Respond with a short motivational message (2–3 lines) using CBT (cognitive behavioral therapy) principles. Be empathetic and supportive.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if available
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=100
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return "You're doing great. Take one step at a time — you're not alone in this."
