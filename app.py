import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import tempfile

st.set_page_config(page_title="Speech App", page_icon="🎤")

st.title("🎤 Voice to Text & 🔊 Text to Voice")

# -------------------------
# Text to Voice
# -------------------------
st.header("Text to Voice")

text = st.text_area("Enter text")

if st.button("Convert Text to Speech"):
    if text:
        tts = gTTS(text=text, lang="en")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)

            audio_file = open(fp.name, "rb")
            audio_bytes = audio_file.read()

        st.audio(audio_bytes, format="audio/mp3")
    else:
        st.warning("Please enter some text.")

# -------------------------
# Voice to Text
# -------------------------
st.header("Voice to Text")

audio_file = st.file_uploader(
    "Upload WAV audio file",
    type=["wav"]
)

if audio_file is not None:
    recognizer = sr.Recognizer()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_file.read())

        with sr.AudioFile(temp_audio.name) as source:
            audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data)
            st.success("Recognized Text:")
            st.write(text)

        except sr.UnknownValueError:
            st.error("Could not understand audio.")

        except sr.RequestError:
            st.error("Speech recognition service unavailable.")
