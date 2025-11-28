import streamlit as st

st.set_page_config(page_title="MindCare", layout="wide")


st.markdown(
    '<div style="background-color:#1E90FF;padding:40px;border-radius:10px;text-align:center;"><h1 style="color:white; font-size:60px;">MindCare 🤖</h1></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<h2 style="text-align:center; color:black; font-size:30px;">Invest in Your Inner Well-being</h2>',
    unsafe_allow_html=True,
)
st.markdown("---")

button_style = """
<style>
.stButton>button {
    background-color: #1E90FF;
    color: white;
    padding: 35px 80px;
    border-radius: 25px;
    border: none;
    font-size: 36px;
    cursor: pointer;
    transition: 0.3s;
    width: 100%;
}
.stButton>button:hover {
    background-color: #187bcd;
}
.button-container {
    display: flex;
    justify-content: center;
    gap: 50px;
}
</style>
"""
st.markdown(button_style, unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("MindCare Assistant", key="mindcare_button"):
        st.switch_page("pages/mindcare_assistant.py")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("AI Doctor Diagnose", key="ai_doctor_button"):
        st.switch_page("pages/ai_diagose.py")

    st.markdown("</div>", unsafe_allow_html=True)


st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

adv_col, video_col = st.columns([1, 1])

with adv_col:
    st.markdown("### Advantages of MindCare Assistant")
    st.markdown(
        "<ul style='font-size:25px;'>\
    <li>Provides personalized mental health support</li>\
    <li>Available 24/7</li>\
    <li>Offers AI-driven guidance and advice</li>\
    </ul>",
        unsafe_allow_html=True,
    )

with video_col:
    st.markdown("### Watch MindCare in Action")
    st.video(
        "/Users/yebhonelin/Documents/github/FTL_Myanmar_Gr5/src/docs/medical_assistant_vd.mov",
        format="video/mp4",
        start_time=0,
        autoplay=True,
        muted=True,
    )

st.write("---")

video_col, adv_col = st.columns([1, 1])

with adv_col:
    st.markdown("### Advantages of AI Doctor Diagnose")

    st.markdown(
        """
    <ul style='font-size:22px; line-height:1.6;'>
        <li>Provides personalized mental health support</li>
        <li>Available 24/7</li>
        <li>Offers AI-driven guidance and advice</li>
        <li>Gives instant responses without waiting</li>
        <li>Helps with early detection of symptoms</li>
        <li>Supports users in remote or rural areas</li>
        <li>Reduces unnecessary clinic visits</li>
    </ul>
    """,
        unsafe_allow_html=True,
    )


with video_col:
    st.markdown("### Watch AI Doctor Diagnose in Action")
    st.video(
        "/Users/yebhonelin/Documents/github/FTL_Myanmar_Gr5/src/docs/ai_diagonse.mov",
        format="video/mp4",
        start_time=0,
        autoplay=True,
        muted=True,
    )
