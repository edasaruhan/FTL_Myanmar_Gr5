import streamlit as st
import requests
import pyttsx3
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
from pydub import AudioSegment

# -------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------
st.set_page_config(page_title="AI Doctor Diagnose", layout="wide")

recognizer = sr.Recognizer()

tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)

st.markdown(
    '<div style="background-color:#1E90FF;padding:20px;border-radius:10px;text-align:center;">'
    '<h1 style="color:white;">AI Doctor Diagnose 🤖</h1></div>',
    unsafe_allow_html=True
)
st.markdown("<h3 style='text-align:center; color:black;'>Speak your symptoms and wait for the doctor</h3>",
            unsafe_allow_html=True)
st.markdown("---")

# -------------------------------------------------
# Session State
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_audio_processed" not in st.session_state:
    st.session_state.last_audio_processed = None

# -------------------------------------------------
# Voice Input Section
# -------------------------------------------------
st.write("### 🎤 Voice Input")
audio_data = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="🛑 Stop Recording",
    key="recorder",
    use_container_width=True
)

if audio_data and audio_data != st.session_state.last_audio_processed:

    st.session_state.last_audio_processed = audio_data

    # Preview audio in UI
    st.audio(audio_data["bytes"])

    # -------------------------------------------------
    # Convert Browser WebM → WAV for SpeechRecognition
    # -------------------------------------------------
    with open("temp_input.webm", "wb") as f:
        f.write(audio_data["bytes"])

    try:
        sound = AudioSegment.from_file("temp_input.webm", format="webm")
        sound = sound.set_frame_rate(16000).set_channels(1)
        sound.export("temp_audio.wav", format="wav")
    except Exception as e:
        st.error(f"❌ Audio conversion failed: {e}")
        st.stop()

    # -------------------------------------------------
    # Speech Recognition
    # -------------------------------------------------
    user_text = ""
    try:
        with sr.AudioFile("temp_audio.wav") as source:
            audio = recognizer.record(source)
            user_text = recognizer.recognize_google(audio, language="en-US")
            st.success(f"**Recognized Speech:** {user_text}")
    except Exception as e:
        st.error(f"❌ Speech could not be recognized: {e}")
        user_text = ""

    # -------------------------------------------------
    # Send text to AI Backend
    # -------------------------------------------------
    if user_text.strip():
        st.session_state.messages.append({"role": "user", "content": user_text})

        api_url = "http://127.0.0.1:8000/Mic_Chat"
        payload = {"user_input": user_text}

        try:
            r = requests.post(api_url, json=payload)
            if r.status_code == 200:
                ai_reply = r.json().get("response", "No response received.")
            else:
                ai_reply = f"Error: {r.status_code}"
        except Exception as e:
            ai_reply = f"Request failed: {e}"

        # Save assistant reply
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})

        # -------------------------------------------------
        # Text-to-Speech
        # -------------------------------------------------
        try:
            tts_engine.say(ai_reply)
            tts_engine.runAndWait()
            st.success("🗣️ Doctor has responded via voice")
        except:
            st.warning("Voice output unavailable.")

# -------------------------------------------------
# Chat History UI
# -------------------------------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"<p style='text-align:right; background:#d9eaff; padding:10px; border-radius:10px;'>"
            f"<b>You:</b> {msg['content']}</p>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<p style='text-align:left; background:#f0f0f0; padding:10px; border-radius:10px;'>"
            f"<b>Doctor:</b> {msg['content']}</p>",
            unsafe_allow_html=True
        )
