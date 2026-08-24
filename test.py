import streamlit as st

st.set_page_config(
    page_title="Lecture Search",
    page_icon="🎓",
    layout="wide"
)

st.markdown(
    """
    <style>
        .title {
            color: white;
            font-size: 32px;
            font-weight: 700;
        }

        .subtitle {
            color: #9ca3af;
            font-size: 15px;
            margin-bottom: 30px;
        }

        .box {
            background: #111827;
            padding: 20px;
            border-radius: 12px;
            color: white;
        }
    </style>

    <div class="title">
        Lecture Search
    </div>

    <div class="subtitle">
        Ask in Hinglish or English. Answers come only from your lectures.
    </div>

    <div class="box">
        HTML is rendering correctly.
    </div>
    """,
    unsafe_allow_html=True
)

question = st.text_input(
    "Ask your question",
    placeholder="ransom note kaha solve hua hai"
)

if st.button("Ask"):
    st.write("Question:", question)