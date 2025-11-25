import streamlit as st
import requests

st.set_page_config(page_title="Medical Assistant")

st.markdown('<div style="background-color:#1E90FF;padding:20px;border-radius:10px;text-align:center;"><h1 style="color:white;">Medical Assistant 🤖</h1></div>', unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:black;'>Ask any medical question below</h3>", unsafe_allow_html=True)
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("You:")

if st.button("Send"):
    if user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        api_url = "http://127.0.0.1:8000/Medical_Chat"
        payload = {"user_input": user_input}
        try:
            response = requests.post(api_url, json=payload)
            if response.status_code == 200:
                ai_reply = response.json().get("response", "Sorry, no response received.")
            else:
                ai_reply = f"Error: {response.status_code}"
        except Exception as e:
            ai_reply = f"Request failed: {e}"
        
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<p style='text-align:right; background:#d9eaff; padding:10px; border-radius:10px;'><b>You:</b> {msg['content']}</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='text-align:left; background:#f0f0f0; padding:10px; border-radius:10px;'><b>Assistant:</b> {msg['content']}</p>", unsafe_allow_html=True)

