
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
