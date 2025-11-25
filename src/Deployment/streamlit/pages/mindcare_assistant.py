import streamlit as st

st.set_page_config(page_title="MindCare Assistant")

st.markdown('<div style="background-color:#1E90FF;padding:20px;border-radius:10px;text-align:center;"><h1 style="color:white;">MindCare Assistant 🤖</h1></div>', unsafe_allow_html=True)

st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("You:")

if st.button("Send"):
    if user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input})
        # Placeholder AI response
        ai_reply = "Thank you for sharing. I'm here to support you."
        st.session_state.messages.append({"role": "MindCare", "content": ai_reply})

# Display messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<p style='text-align:right; background:#d9eaff; padding:10px; border-radius:10px;'><b>You:</b> {msg['content']}</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='text-align:left; background:#f0f0f0; padding:10px; border-radius:10px;'><b>Assistant:</b> {msg['content']}</p>", unsafe_allow_html=True)

