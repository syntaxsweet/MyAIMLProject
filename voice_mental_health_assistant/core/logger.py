# core/logger.py
import csv
from datetime import datetime
import os

LOG_FILE = "logs/emotion_log.csv"

def save_log(transcription, emotion, score, feedback):
    os.makedirs("logs", exist_ok=True)  # Ensure logs folder exists

    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().isoformat(), transcription, emotion, round(score, 4), feedback])
