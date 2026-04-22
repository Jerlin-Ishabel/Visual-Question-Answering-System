import speech_recognition as sr # type: ignore
from gtts import gTTS # type: ignore
import tempfile
import os
import streamlit as st

LANG_MAP = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Malayalam": "ml",
    "Telugu": "te"
}


# ============================
# VOICE INPUT (ALWAYS ENGLISH)
# ============================
def get_voice_input(language="English"):

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            st.info("🎙 Listening...")
            audio = recognizer.listen(source)

        # 🔥 Always English recognition
        text = recognizer.recognize_google(audio, language="en-IN")
        return text

    except Exception:
        st.error("Voice input failed.")
        return None


# ============================
# VOICE OUTPUT (Selected Language)
# ============================
def speak_answer(text, language):

    try:
        lang_code = LANG_MAP.get(language, "en")

        tts = gTTS(text=text, lang=lang_code)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            audio_path = fp.name

        with open(audio_path, "rb") as f:
            audio_bytes = f.read()

        st.audio(audio_bytes, format="audio/mp3")

        os.remove(audio_path)

    except Exception:
        st.warning("Voice output failed.")
