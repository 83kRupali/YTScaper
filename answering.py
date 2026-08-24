# import os

# from dotenv import load_dotenv
# from groq import Groq


# # ============================================================
# # ENVIRONMENT
# # ============================================================

# load_dotenv(
#     override=True
# )


# GROQ_API_KEY = os.getenv(
#     "GROQ_API_KEY"
# )


# # ============================================================
# # GROQ CLIENT
# # ============================================================

# groq_client = Groq(
#     api_key=GROQ_API_KEY
# )


# # ============================================================
# # GENERATE ANSWER
# # ============================================================

# def generate_answer(
#     question,
#     retrieved_chunks
# ):

#     # --------------------------------------------------------
#     # Build context
#     # --------------------------------------------------------

#     context_parts = []


#     for i, result in enumerate(
#         retrieved_chunks,
#         start=1
#     ):

#         payload = result.payload


#         context_parts.append(
#             f"""
# SOURCE {i}

# Video ID:
# {payload.get("video_id")}

# Title:
# {payload.get("title")}

# Timestamp:
# {payload.get("timestamp")}

# Start:
# {payload.get("start")} seconds

# End:
# {payload.get("end")} seconds

# Text:
# {payload.get("text")}
# """
#         )


#     context = "\n".join(
#         context_parts
#     )


#     # --------------------------------------------------------
#     # RAG PROMPT
#     # --------------------------------------------------------

# #     prompt = f"""
# # You are a YouTube Lecture RAG assistant.

# # Answer the user's question using ONLY the lecture
# # context provided below.

# # Do NOT use outside knowledge.

# # If the answer is not available in the context,
# # say exactly:

# # "I could not find this information in the provided lectures."

# # Important rules:

# # 1. Give a clear and easy-to-understand answer.
# # 2. Use information from the retrieved lectures.
# # 3. Do not invent information.
# # 4. If the lecture gives multiple points, explain them.
# # 5. Mention the relevant video title.
# # 6. Mention the timestamp where the information was discussed.
# # 7. Do not create fake timestamps.
# # 8. Do not create information that is not present in the context.

# # USER QUESTION:

# # {question}


# # LECTURE CONTEXT:

# # {context}
# # """



#     prompt = f"""
# You are a STRICT YouTube Lecture RAG Assistant.

# Your job is to answer the user's question using ONLY the
# lecture context provided below.

# The lecture transcripts may contain speech-to-text errors.
# You may understand obvious transcription mistakes in technical
# words, but you MUST NOT add information that is not present
# in the lectures.

# ==================================================
# STRICT RULES
# ==================================================

# 1. USE ONLY THE PROVIDED CONTEXT
# ---------------------------------
# Answer only from the retrieved lecture transcripts.

# Do NOT use:
# - your general knowledge
# - textbook knowledge
# - internet knowledge
# - information from previous conversations
# - information not present in the context

# If the answer cannot be supported by the context, say exactly:

# "I could not find this information in the provided lectures."


# 2. DO NOT HALLUCINATE
# ---------------------
# Never invent:
# - examples
# - questions
# - algorithms
# - data structures
# - definitions
# - steps
# - code
# - time complexity
# - space complexity
# - explanations
# - timestamps
# - video IDs
# - lecture titles

# Everything in the answer must be supported by the lecture
# context.


# 3. ANSWER EXACTLY WHAT THE USER ASKED
# --------------------------------------
# Do not turn a simple question into a long DSA tutorial.

# For example, if the user asks:

# "What is two pointer?"

# Give the definition/explanation available in the lecture.

# If the user asks:

# "When should I use two pointer?"

# Give only the conditions mentioned in the lecture.

# If the user asks:

# "Give a two pointer question"

# ONLY provide a question if the retrieved lecture actually
# contains a question/example.

# DO NOT create a standard DSA question from your own knowledge.


# 4. SOURCE SELECTION
# -------------------
# Use the most relevant lecture source first.

# If one source completely answers the question, prefer that
# source instead of unnecessarily combining unrelated sources.

# Use multiple sources only when they directly provide different
# parts of the answer.

# Do NOT combine unrelated lectures just because they contain
# similar words.


# 5. SOURCE INFORMATION
# ---------------------
# When answering, mention the relevant:

# - Video Title
# - Video ID
# - Timestamp

# Use ONLY the metadata provided in the context.

# Never invent or modify timestamps.


# 6. CITATIONS
# ------------
# Every important factual statement should have a source citation.

# Use the source number exactly as provided:

# [1]
# [2]
# [3]

# Never create a citation number that does not exist.


# 7. TRANSCRIPT ERRORS
# --------------------
# The transcript may contain errors because it was generated
# using speech-to-text.

# You may silently understand obvious errors such as:

# "two pointer" / "two pointers"
# "aray" -> "array"
# "poiner" -> "pointer"
# "link list" -> "linked list"

# But you MUST NOT use this as a reason to introduce new
# technical information.


# 8. LANGUAGE
# -----------
# Answer in the same language/style as the user's question.

# English question -> English answer.

# Hindi question -> Hindi answer.

# Hinglish question -> Hinglish answer.


# 9. ANSWER FORMAT
# ----------------
# Keep the answer clear and concise.

# Use this format when the information is available:

# Answer:
# <direct answer>

# Explanation:
# <short explanation based only on the lecture>

# Lecture Source:
# <Video Title>
# Timestamp: <timestamp>

# Use bullets when they make the explanation easier to understand.

# Do NOT create a table unless the user explicitly asks for one.


# 10. NO EXTRA INFORMATION
# ------------------------
# After answering the question, STOP.

# Do not add:
# - "You should also learn..."
# - "In general..."
# - "According to DSA..."
# - textbook examples
# - additional algorithms
# - additional complexity analysis
# - unrelated concepts


# 11. FINAL VERIFICATION
# ----------------------
# Before generating the answer, check:

# - Is every claim supported by the context?
# - Did I use outside knowledge?
# - Did I invent an example?
# - Did I invent a question?
# - Did I invent a timestamp?
# - Did I invent complexity?
# - Did I mix unrelated videos?
# - Did I answer exactly what the user asked?

# If any information is not supported by the context,
# REMOVE it.

# If the context does not contain enough information, respond:

# "I could not find this information in the provided lectures."


# ==================================================
# USER QUESTION
# ==================================================

# {question}


# ==================================================
# LECTURE CONTEXT
# ==================================================

# {context}
# """
#     # --------------------------------------------------------
#     # CALL GROQ
#     # --------------------------------------------------------

#     response = groq_client.chat.completions.create(

#         model="openai/gpt-oss-120b",

#         messages=[

#             {
#                 "role": "system",

#                 "content":
#                     "You are a strict lecture-based RAG assistant."
#             },

#             {
#                 "role": "user",

#                 "content":
#                     prompt
#             }

#         ],

#         temperature=0
#     )


#     return (
#         response
#         .choices[0]
#         .message
#         .content
#     )





































import os

from dotenv import load_dotenv
from groq import Groq


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)


# ============================================================
# GROQ CLIENT
# ============================================================

groq_client = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(
    question,
    results
):

    # --------------------------------------------------------
    # No relevant results
    # --------------------------------------------------------

    if not results:

        return (
            "I could not find this information "
            "in the provided lectures."
        )


    # --------------------------------------------------------
    # BUILD STRICT CONTEXT
    # --------------------------------------------------------

    context_parts = []


    for index, item in enumerate(
        results,
        start=1
    ):

        # ----------------------------------------------------
        # retrieval.py returns:
        #
        # (reranker_score, qdrant_result)
        # ----------------------------------------------------

        rerank_score, result = item

        payload = result.payload


        video_id = payload.get(
            "video_id",
            "Unknown"
        )

        title = payload.get(
            "title",
            "Unknown"
        )

        language = payload.get(
            "language",
            "Unknown"
        )

        timestamp = payload.get(
            "timestamp",
            "Unknown"
        )

        start = payload.get(
            "start",
            ""
        )

        end = payload.get(
            "end",
            ""
        )

        video_url = payload.get(
            "video_url",
            ""
        )

        text = payload.get(
            "text",
            ""
        )


        context_parts.append(
            f"""
==================================================
SOURCE [{index}]
==================================================

Video ID:
{video_id}

Title:
{title}

Language:
{language}

Timestamp:
{timestamp}

Start:
{start}

End:
{end}

Video URL:
{video_url}

Transcript:
{text}

Reranker relevance score:
{rerank_score:.4f}
"""
        )


    context = "\n".join(
        context_parts
    )


    # ========================================================
    # STRICT RAG PROMPT
    # ========================================================

    prompt = f"""
You are a STRICT YouTube Lecture RAG assistant.

Your job is to answer the user's question ONLY from
the transcript sources provided below.

You are NOT a general-purpose AI assistant.

You MUST follow these rules.

==================================================
RULE 1 — USE ONLY LECTURE CONTENT
==================================================

Use ONLY information explicitly present in the
provided transcript sources.

Do NOT use your own knowledge.

Do NOT complete missing information from memory.

Do NOT assume what the lecturer meant.

Do NOT add standard textbook knowledge unless it
is explicitly present in the transcript.

==================================================
RULE 2 — RELEVANCE
==================================================

Only use a source if its transcript actually
answers or directly supports the user's question.

Do NOT use a source just because it contains
similar words.

For example:

Question:
"What is the basic two pointer approach?"

A transcript about "heap" is NOT relevant even if
it contains words such as "pointer", "array", etc.

==================================================
RULE 3 — NO HALLUCINATION
==================================================

Never invent:

- algorithms
- examples
- code
- complexity
- definitions
- explanations
- video titles
- timestamps
- video IDs
- URLs

If the required information is not present in the
provided transcripts, respond EXACTLY:

"I could not find this information in the provided lectures."

==================================================
RULE 4 — SOURCE CITATION
==================================================

Every important claim must have a source citation.

Use:

[1]
[2]
[3]

The number must correspond to the SOURCE number.

Example:

The lecturer explains that two pointers are useful
when working with sorted arrays. [1]

==================================================
RULE 5 — VIDEO INFORMATION
==================================================

When the answer is supported by a source, mention:

- lecture title
- timestamp

Only use the title and timestamp that appear in
the source.

==================================================
RULE 6 — DO NOT MIX UNRELATED SOURCES
==================================================

If SOURCE [1] answers the question, do not add
information from SOURCE [2] unless SOURCE [2]
also directly supports the answer.

==================================================
RULE 7 — QUESTION TYPE
==================================================

First understand what the user is asking.

If the user asks:

"what is..."
→ give the definition/explanation from the lecture.

If the user asks:

"how..."
→ explain the steps given in the lecture.

If the user asks:

"why..."
→ explain only the reason given in the lecture.

If the user asks:

"give a question..."
→ provide a question only if the lecture
contains or clearly describes that problem.

Do NOT create a new problem unless the lecture
itself provides one.

==================================================
RULE 8 — LANGUAGE
==================================================

Answer in the same language style as the question.

English question:
→ English answer.

Hindi/Hinglish question:
→ Hindi/Hinglish answer.

==================================================
RULE 9 — CONCISE ANSWER
==================================================

Give a focused answer.

Do not unnecessarily discuss unrelated
lecture material.

==================================================
USER QUESTION
==================================================

{question}


==================================================
LECTURE SOURCES
==================================================

{context}


==================================================
FINAL INSTRUCTION
==================================================

Answer the user's question using ONLY the relevant
lecture source(s).

If none of the sources actually contain the answer,
respond exactly:

"I could not find this information in the provided lectures."
"""


    # ========================================================
    # CALL GROQ
    # ========================================================

    response = groq_client.chat.completions.create(

        model="openai/gpt-oss-120b",

        temperature=0,

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict retrieval-augmented "
                    "generation assistant. "
                    "Never use information outside "
                    "the supplied lecture context."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    # ========================================================
    # RETURN ANSWER
    # ========================================================

    return response.choices[0].message.content.strip()