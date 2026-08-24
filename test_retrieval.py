from retrieval import retrieve_chunks


print("\n====================================")
print("🔎 YOUTUBE LECTURE RETRIEVAL")
print("====================================")


question = input(
    "\nEnter your question: "
)


results = retrieve_chunks(
    question,
    top_k=5
)


print("\n====================================")
print("📚 RETRIEVED CHUNKS")
print("====================================")


if not results:

    print(
        "❌ No relevant chunks found."
    )


for i, item in enumerate(
    results,
    start=1
):

    rerank_score, result = item

    payload = result.payload


    print(
        f"\n{'=' * 60}"
    )

    print(
        f"SOURCE {i}"
    )

    print(
        f"{'=' * 60}"
    )


    print(
        f"Score      : {result.score:.4f}"
    )

    print(
        f"Video ID   : "
        f"{payload.get('video_id')}"
    )

    print(
        f"Title      : "
        f"{payload.get('title')}"
    )

    print(
        f"Language   : "
        f"{payload.get('language')}"
    )

    print(
        f"Timestamp  : "
        f"{payload.get('timestamp')}"
    )

    print(
        f"Start      : "
        f"{payload.get('start')} sec"
    )

    print(
        f"End        : "
        f"{payload.get('end')} sec"
    )

    print(
        f"Video URL  : "
        f"{payload.get('video_url')}"
    )

    print(
        "\nText:"
    )

    print(
        payload.get("text")
    )



