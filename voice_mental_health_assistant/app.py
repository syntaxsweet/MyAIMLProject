# app.py
import pandas as pd

import streamlit as st
from core.stt import transcribe_audio
from core.emotion import detect_emotion
from core.feedback import generate_feedback
from core.logger import save_log

st.set_page_config(page_title="🧠 Voice Mental Health Assistant", layout="centered")
st.title("🧠 Voice-Based Mental Health Assistant")
st.markdown("Upload your voice and receive emotional insights + CBT-style feedback 🌱")

# Upload audio file
audio_file = st.file_uploader("🎙 Upload a short voice note (WAV/MP3)", type=["wav", "mp3"])

if audio_file is not None:
    # Save the uploaded audio to a temporary file
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_file.read())

    st.audio("temp_audio.wav", format="audio/wav")
    st.info("🔁 Processing your voice...")

    # 1. Transcribe audio
    text = transcribe_audio("temp_audio.wav")

    # 2. Detect emotion
    emotion, score = detect_emotion(text)

    # 3. Generate feedback
    response = generate_feedback(emotion)

    # 4. Save the session to logs
    save_log(text, emotion, score, response)

    # 5. Display the results
    st.markdown("### 📝 Transcription")
    st.success(text)

    st.markdown("### 💬 Detected Emotion")
    st.info(f"**{emotion}** ({round(score * 100, 2)}% confidence)")

    st.markdown("### 🌱 Motivational Feedback")
    st.success(response)
# 🧭 Show Emotional Trend Chart (Optional)
st.markdown("## 📈 Emotional Trend Over Time")

if st.button("Show Mood Chart"):
    try:
        df = pd.read_csv("logs/emotion_log.csv", header=None)
        df.columns = ["timestamp", "transcription", "emotion", "score", "feedback"]
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        # Convert emotion labels into numeric scores (for visualization only)
        emotion_mapping = {
            "joy": 1,
            "love": 2,
            "gratitude": 3,
            "neutral": 4,
            "surprise": 5,
            "sadness": -1,
            "fear": -2,
            "anger": -3,
            "anxiety": -4
        }
        df["emotion_score"] = df["emotion"].str.lower().map(emotion_mapping).fillna(0)

        st.line_chart(df.set_index("timestamp")["emotion_score"])

        st.caption("🧠 Higher is positive emotion, lower is negative.")
    except Exception as e:
        st.warning("No log data found yet. Try uploading a voice file first.")
