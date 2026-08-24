import streamlit as st

from rag import run_rag


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Lecture Search",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "answer" not in st.session_state:
    st.session_state.answer = None

if "results" not in st.session_state:
    st.session_state.results = []

if "selected_index" not in st.session_state:
    st.session_state.selected_index = 0


# ============================================================
# DARK THEME
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #080b0f;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 30px;
    }

    h1, h2, h3 {
        color: #d1d5db !important;
    }

    p, label {
        color: #d1d5db !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.title("Lecture Search")

st.caption(
    "Ask in Hinglish or English. "
    "Answers come only from what was actually said in the lectures."
)

st.divider()


# ============================================================
# SEARCH AREA
# ============================================================

search_col, button_col = st.columns(
    [6, 1],
    vertical_alignment="bottom"
)

with search_col:

    question = st.text_input(
        "Ask your question",
        placeholder="ransom note kaha solve hua hai",
        label_visibility="collapsed"
    )


with button_col:

    ask = st.button(
        "Ask",
        type="primary",
        use_container_width=True
    )


# ============================================================
# RUN RAG
# ============================================================

if ask:

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Searching lectures..."
        ):

            answer, results = run_rag(
                question.strip()
            )

        st.session_state.answer = answer
        st.session_state.results = results
        st.session_state.selected_index = 0


# ============================================================
# GET RESULTS
# ============================================================

results = st.session_state.results


# ============================================================
# MAIN CONTENT
# ============================================================

if results:

    # ========================================================
    # SELECTED VIDEO
    # ========================================================

    selected_item = results[
        st.session_state.selected_index
    ]

    # Handle:
    # (rerank_score, result)
    if isinstance(selected_item, tuple):

        rerank_score, selected_result = selected_item

    else:

        rerank_score = None
        selected_result = selected_item


    payload = selected_result.payload


    video_id = payload.get(
        "video_id",
        ""
    )

    title = payload.get(
        "title",
        "Unknown Lecture"
    )

    timestamp = payload.get(
        "timestamp",
        "00:00"
    )

    start = payload.get(
        "start",
        0
    )

    language = payload.get(
        "language",
        "unknown"
    )

    score = selected_result.score


    # ========================================================
    # VIDEO + ANSWER AREA
    # ========================================================

    left_col, right_col = st.columns(
        [1.15, 0.95],
        gap="large"
    )


    # ========================================================
    # LEFT - ANSWER
    # ========================================================

    with left_col:

        st.subheader("💡 Answer")

        st.markdown(
            st.session_state.answer
        )


        st.divider()


        st.subheader("Sources")


        # ====================================================
        # SOURCE LIST
        # ====================================================

        for i, item in enumerate(
            results
        ):

            if isinstance(item, tuple):

                rerank, result = item

            else:

                rerank = None
                result = item


            source_payload = result.payload


            source_title = source_payload.get(
                "title",
                "Unknown Lecture"
            )

            source_timestamp = source_payload.get(
                "timestamp",
                "00:00"
            )

            source_video_id = source_payload.get(
                "video_id",
                ""
            )

            source_start = int(
                source_payload.get(
                    "start",
                    0
                )
            )


            # -----------------------------------------------
            # Source container
            # -----------------------------------------------

            with st.container(
                border=True
            ):

                source_col1, source_col2 = st.columns(
                    [6, 1]
                )


                with source_col1:

                    st.markdown(
                        f"**[{i + 1}] {source_title}**"
                    )

                    st.caption(
                        f"⏱ {source_timestamp}   "
                        f"•   Video ID: `{source_video_id}`"
                    )


                with source_col2:

                    if st.button(
                        "▶",
                        key=f"play_{i}",
                        help="Play this lecture source"
                    ):

                        st.session_state.selected_index = i

                        st.rerun()


                # -------------------------------------------
                # Transcript
                # -------------------------------------------

                with st.expander(
                    "View transcript"
                ):

                    st.write(
                        source_payload.get(
                            "text",
                            ""
                        )
                    )


    # ========================================================
    # RIGHT - YOUTUBE PLAYER
    # ========================================================

    with right_col:

        st.subheader("# Lecture Player")

        st.video(
            f"https://www.youtube.com/watch?v={video_id}",
            start_time=int(start)
        )


        st.markdown(
            f"**{title}**"
        )

        st.caption(
            f"⏱ {timestamp}  •  "
            f"Language: {language}"
        )


        # ====================================================
        # WATCH BUTTON
        # ====================================================

        youtube_url = (
            f"https://www.youtube.com/watch?v="
            f"{video_id}"
            f"&t={int(start)}s"
        )


        st.link_button(
            "▶ Watch on YouTube",
            youtube_url,
            use_container_width=True
        )


        # ====================================================
        # SCORE
        # ====================================================

        st.divider()

        st.caption(
            f"Similarity Score: {score:.4f}"
        )

        if rerank_score is not None:

            st.caption(
                f"Rerank Score: {rerank_score:.4f}"
            )


# ============================================================
# NO RESULTS
# ============================================================

elif st.session_state.answer:

    st.subheader(" Answer")

    st.write(
        st.session_state.answer
    )

    st.info(
        "No lecture sources were retrieved."
    )





