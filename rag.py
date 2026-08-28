from retrieval import retrieve_chunks
from answering import generate_answer


# ============================================================
# DISPLAY SOURCES
# ============================================================

def display_sources(results):

    print("\n====================================")
    print("📚 SOURCES")
    print("====================================")

    if not results:

        print(
            "No relevant lecture sources found."
        )

        return


    for i, item in enumerate(
        results,
        start=1
    ):

        # ----------------------------------------------------
        # Get reranker score + Qdrant result
        # ----------------------------------------------------

        rerank_score, result = item

        payload = result.payload


        print(
            f"\n[{i}]"
        )

        print(
            f"Qdrant Score : "
            f"{result.score:.4f}"
        )

        print(
            f"Rerank Score : "
            f"{rerank_score:.4f}"
        )

        print(
            f"Video ID     : "
            f"{payload.get('video_id')}"
        )

        print(
            f"Title        : "
            f"{payload.get('title')}"
        )

        print(
            f"Language     : "
            f"{payload.get('language')}"
        )

        print(
            f"Timestamp    : "
            f"{payload.get('timestamp')}"
        )

        print(
            f"Start        : "
            f"{payload.get('start')}"
        )

        print(
            f"End          : "
            f"{payload.get('end')}"
        )

        print(
            f"URL          : "
            f"{payload.get('video_url')}"
        )

        print(
            f"Text         : "
            f"{payload.get('text', '')[:500]}"
        )


# ============================================================
# RUN RAG
# ============================================================

def run_rag(question):

    # --------------------------------------------------------
    # Qdrant + CrossEncoder
    # --------------------------------------------------------

    try:
        results = retrieve_chunks(

            question,

            top_k=10,

            final_k=3
        )
    except RuntimeError as error:
        return str(error), []


    # --------------------------------------------------------
    # No results
    # --------------------------------------------------------

    if not results:

        return (
            "I could not find this information "
            "in the provided lectures.",
            []
        )


    # --------------------------------------------------------
    # LLM answer
    # --------------------------------------------------------

    answer = generate_answer(

        question,

        results
    )


    return answer, results


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "\n===================================="
    )

    print(
        "🎓 YouTube Lecture RAG"
    )

    print(
        "===================================="
    )


    question = input(
        "\nAsk your question: "
    ).strip()


    if not question:

        print(
            "\n❌ Please enter a question."
        )

        return


    answer, results = run_rag(
        question
    )


    # --------------------------------------------------------
    # ANSWER
    # --------------------------------------------------------

    print(
        "\n===================================="
    )

    print(
        "💡 ANSWER"
    )

    print(
        "====================================\n"
    )

    print(answer)


    # --------------------------------------------------------
    # SOURCES
    # --------------------------------------------------------

    display_sources(
        results
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
