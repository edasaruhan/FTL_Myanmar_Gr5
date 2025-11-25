import streamlit as st
import requests
import pyttsx3
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="AI Doctor Diagnose", layout="wide")

# --- Initialize recognizer ---
recognizer = sr.Recognizer()

# --- Initialize TTS ---
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)

# --- Streamlit Header ---
st.markdown(
    '<div style="background-color:#1E90FF;padding:20px;border-radius:10px;text-align:center;">'
    '<h1 style="color:white;">AI Doctor Diagnose 🤖</h1></div>', 
    unsafe_allow_html=True
)
st.markdown("<h3 style='text-align:center; color:black;'>Speak your symptoms and wait for the doctor</h3>", unsafe_allow_html=True)
st.markdown("---")

# --- Chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_audio_processed" not in st.session_state:
    st.session_state.last_audio_processed = None


# --- Microphone Recorder ---
st.write("### 🎤 Voice Input")
audio_data = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="🛑 Stop Recording",
    key="recorder",
    use_container_width=True
)

# When recording stops
if audio_data and audio_data != st.session_state.last_audio_processed:

    st.session_state.last_audio_processed = audio_data  # Avoid double-processing
    st.audio(audio_data["bytes"], format="audio/wav")

    # Save temp file
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_data["bytes"])

    # --- Convert Speech to Text ---
    user_text = ""
    try:
        with sr.AudioFile("temp_audio.wav") as source:
            audio = recognizer.record(source)
            user_text = recognizer.recognize_google(audio, language="en-US")
            st.success(f"**Recognized Speech:** {user_text}")

    except Exception as e:
        st.error("❌ Speech could not be understood.")
        user_text = ""

    # --- If STT success: send to API ---
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

        # Save doctor reply
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})

        # --- TEXT TO SPEECH ---
        tts_engine.say(ai_reply)
        tts_engine.runAndWait()

        st.success("🗣️ Doctor has responded via voice")


# --- Chat UI ---
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
