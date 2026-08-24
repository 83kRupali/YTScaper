from embedding import create_query_embedding
from qdrant_store import client, COLLECTION_NAME

from sentence_transformers import CrossEncoder


# ============================================================
# LOAD CROSS-ENCODER RERANKER
# ============================================================

print("Loading CrossEncoder reranker...")

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

print("CrossEncoder ready!")


# ============================================================
# RETRIEVE + RERANK RELEVANT CHUNKS
# ============================================================

def retrieve_chunks(
    question,
    top_k=10,
    final_k=3
):

    # --------------------------------------------------------
    # 1. Convert question into embedding
    # --------------------------------------------------------

    query_vector = create_query_embedding(
        question
    )


    # --------------------------------------------------------
    # 2. Qdrant semantic search
    #
    # Get MORE candidates first.
    # We don't directly trust these results.
    # --------------------------------------------------------

    try:
        response = client.query_points(

            collection_name=COLLECTION_NAME,

            query=query_vector,

            limit=top_k,

            with_payload=True,

            with_vectors=False
        )
    except Exception as error:
        raise RuntimeError(
            "Unable to reach Qdrant. Check QDRANT_URL, "
            "internet/DNS access, and the Qdrant service status."
        ) from error


    candidates = response.points


    # --------------------------------------------------------
    # 3. No results
    # --------------------------------------------------------

    if not candidates:
        return []


    # --------------------------------------------------------
    # 4. Prepare Question + Transcript pairs
    # --------------------------------------------------------

    pairs = []

    valid_candidates = []

    for result in candidates:

        text = result.payload.get(
            "text",
            ""
        )

        if not text.strip():
            continue


        pairs.append(
            [
                question,
                text
            ]
        )

        valid_candidates.append(
            result
        )


    if not pairs:
        return []


    # --------------------------------------------------------
    # 5. CrossEncoder reranking
    #
    # This checks:
    #
    # QUESTION
    #     +
    # TRANSCRIPT
    #
    # and gives a relevance score.
    # --------------------------------------------------------

    rerank_scores = reranker.predict(
        pairs
    )


    # --------------------------------------------------------
    # 6. Combine score + Qdrant result
    # --------------------------------------------------------

    ranked_results = []

    for score, result in zip(
        rerank_scores,
        valid_candidates
    ):

        ranked_results.append(
            (
                float(score),
                result
            )
        )


    # --------------------------------------------------------
    # 7. Sort by CrossEncoder score
    # --------------------------------------------------------

    ranked_results.sort(
        key=lambda x: x[0],
        reverse=True
    )


    # --------------------------------------------------------
    # 8. Return only BEST chunks
    # --------------------------------------------------------

    final_results = ranked_results[
        :final_k
    ]


    return final_results