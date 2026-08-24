import os

from dotenv import load_dotenv

from qdrant_client import QdrantClient

from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    PayloadSchemaType
)


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv(
    override=True
)


QDRANT_URL = os.getenv(
    "QDRANT_URL"
)

QDRANT_API_KEY = os.getenv(
    "QDRANT_API_KEY"
)


# ============================================================
# COLLECTION
# ============================================================

COLLECTION_NAME = (
    "youtube_lecture_rag_v2"
)


# ============================================================
# CONNECT
# ============================================================

client = QdrantClient(

    url=QDRANT_URL,

    api_key=QDRANT_API_KEY,

    timeout=120
)


print(
    "✅ Connected to Qdrant"
)


# ============================================================
# CREATE COLLECTION
# ============================================================

def create_collection(
    vector_size
):

    if client.collection_exists(
        COLLECTION_NAME
    ):

        print(
            f"Collection already exists: "
            f"{COLLECTION_NAME}"
        )

        return


    client.create_collection(

        collection_name=
            COLLECTION_NAME,

        vectors_config=
            VectorParams(

                size=vector_size,

                distance=
                    Distance.COSINE
            )
    )


    # --------------------------------------------------------
    # Metadata indexes
    # --------------------------------------------------------

    client.create_payload_index(

        collection_name=
            COLLECTION_NAME,

        field_name="video_id",

        field_schema=
            PayloadSchemaType.KEYWORD
    )


    client.create_payload_index(

        collection_name=
            COLLECTION_NAME,

        field_name="language",

        field_schema=
            PayloadSchemaType.KEYWORD
    )


    print(
        f"✅ Created collection: "
        f"{COLLECTION_NAME}"
    )


# ============================================================
# UPLOAD CHUNKS
# ============================================================

def upload_chunks(
    chunks,
    embeddings
):

    points = []


    for index, (
        chunk,
        embedding
    ) in enumerate(
        zip(chunks, embeddings)
    ):

        point = PointStruct(

            id=index + 1,

            vector=embedding.tolist(),

            payload=chunk
        )


        points.append(
            point
        )


    # --------------------------------------------------------
    # Upload in batches
    # --------------------------------------------------------

    batch_size = 50


    total = len(points)


    for start in range(
        0,
        total,
        batch_size
    ):

        batch = points[
            start:
            start + batch_size
        ]


        print(
            f"Uploading points "
            f"{start + 1}-"
            f"{min(start + batch_size, total)} "
            f"of {total}..."
        )


        client.upsert(

            collection_name=
                COLLECTION_NAME,

            points=batch,

            wait=True
        )


    print(
        f"✅ Uploaded "
        f"{total}/{total}"
    )




    