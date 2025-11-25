import streamlit as st


st.set_page_config(page_title="MindCare", layout="centered")

st.markdown('<div style="background-color:#1E90FF;padding:20px;border-radius:10px;text-align:center;"><h1 style="color:white;">MindCare 🤖</h1></div>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align:center; color:white;"><span style="color:black;">Invest in Your Inner Well-being</span></h3>', unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns(2)

button_style = """
<style>
.custom-button {
background-color: #1E90FF;
color: white;
padding: 15px 25px;
border-radius: 10px;
border: none;
font-size: 18px;
width: 100%;
cursor: pointer;
transition: 0.3s;
}
.custom-button:hover {
background-color: #187bcd;
}
</style>
"""
st.markdown(button_style, unsafe_allow_html=True)


with col1:
    if st.markdown('<button class="custom-button">MindCare Assistant</button>', unsafe_allow_html=True):
        if st.button == True:
            st.switch_page("pages/mindcare_assistant.py")

with col2:
    if st.markdown('<button class="custom-button">AI Doctor Diagnose</button>', unsafe_allow_html=True):
        pass
