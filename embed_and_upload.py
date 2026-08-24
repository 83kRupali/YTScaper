import json

from pathlib import Path

from embedding import (
    create_embeddings,
    get_embedding_dimension
)

from qdrant_store import (
    create_collection,
    upload_chunks
)


# ============================================================
# CONFIG
# ============================================================

CHUNK_DIR = Path(
    "chunks1"
)


# ============================================================
# LOAD ALL CHUNKS
# ============================================================

def load_chunks():

    all_chunks = []


    files = sorted(
        CHUNK_DIR.glob(
            "*_chunks.json"
        )
    )


    print(
        f"Found chunk files: "
        f"{len(files)}"
    )


    for file_path in files:

        print(
            f"Reading: "
            f"{file_path.name}"
        )


        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)


        chunks = data.get(
            "chunks",
            []
        )


        all_chunks.extend(
            chunks
        )


        print(
            f"  Chunks: "
            f"{len(chunks)}"
        )


    return all_chunks


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "\n===================================="
    )

    print(
        "CHUNKS → EMBEDDINGS → QDRANT"
    )

    print(
        "===================================="
    )


    # --------------------------------------------------------
    # 1. Load chunks
    # --------------------------------------------------------

    chunks = load_chunks()


    if not chunks:

        print(
            "❌ No chunks found."
        )

        return


    print(
        f"\nTotal chunks: "
        f"{len(chunks)}"
    )


    # --------------------------------------------------------
    # 2. Extract text
    # --------------------------------------------------------

    texts = [

        chunk["text"]

        for chunk in chunks
    ]


    # --------------------------------------------------------
    # 3. Embeddings
    # --------------------------------------------------------

    print(
        "\nCreating embeddings..."
    )


    embeddings = create_embeddings(
        texts
    )


    print(
        f"✅ Embeddings created: "
        f"{len(embeddings)}"
    )


    # --------------------------------------------------------
    # 4. Vector size
    # --------------------------------------------------------

    vector_size = (
        get_embedding_dimension()
    )


    print(
        f"Embedding dimension: "
        f"{vector_size}"
    )


    # --------------------------------------------------------
    # 5. Create Qdrant collection
    # --------------------------------------------------------

    create_collection(
        vector_size
    )


    # --------------------------------------------------------
    # 6. Upload
    # --------------------------------------------------------

    print(
        "\nUploading to Qdrant..."
    )


    upload_chunks(
        chunks,
        embeddings
    )


    print(
        "\n===================================="
    )

    print(
        "🎉 EMBEDDING + QDRANT COMPLETED"
    )

    print(
        "===================================="
    )


if __name__ == "__main__":

    main()




    