from sentence_transformers import SentenceTransformer


# ============================================================
# EMBEDDING MODEL
# ============================================================

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


print("Loading embedding model...")

model = SentenceTransformer(
    MODEL_NAME
)

print("✅ Embedding model loaded")


# ============================================================
# CREATE EMBEDDINGS
# ============================================================

def create_embeddings(texts):

    embeddings = model.encode(

        texts,

        batch_size=32,

        show_progress_bar=True,

        normalize_embeddings=True
    )

    return embeddings


# ============================================================
# QUERY EMBEDDING
# ============================================================

def create_query_embedding(query):

    embedding = model.encode(

        query,

        normalize_embeddings=True
    )

    return embedding.tolist()


# ============================================================
# EMBEDDING DIMENSION
# ============================================================

def get_embedding_dimension():

    return model.get_sentence_embedding_dimension()



