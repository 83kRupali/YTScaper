# YTScape AI

## Intelligent YouTube Lecture Search & RAG Assistant

YTScape AI is an AI-powered Retrieval-Augmented Generation (RAG) application that allows users to ask questions about YouTube lectures and get answers from the actual lecture content.

The system processes YouTube lecture transcripts, converts them into timestamp-aware chunks, creates vector embeddings, stores them in Qdrant Vector Database, retrieves relevant lecture content, and uses an LLM to generate the final answer.

The system also provides the relevant YouTube video and timestamp so that users can directly watch the lecture from the required point.

---

## Features

- YouTube lecture processing
- Speech-to-text transcription
- Hindi and English transcript support
- Timestamp-aware transcript
- Transcript to JSON conversion
- Text chunking
- Sentence Transformer embeddings
- Qdrant Vector Database
- Semantic search
- Retrieval-Augmented Generation (RAG)
- Groq LLM
- Lecture source retrieval
- YouTube timestamp links
- Streamlit frontend
- English and Hinglish question support

---

## Project Architecture

```text
YouTube Videos
      |
      v
Audio / Transcript
      |
      v
Timestamped JSON
      |
      v
Text Chunking
      |
      v
Sentence Transformer
      |
      v
Embeddings
      |
      v
Qdrant Vector Database
      |
      |
User Question
      |
      v
Query Embedding
      |
      v
Qdrant Retrieval
      |
      v
Relevant Lecture Chunks
      |
      v
Groq LLM
      |
      v
Generated Answer
      |
      +----------------------+
      |                      |
      v                      v
Lecture Sources        YouTube Timestamp
      |                      |
      +----------+-----------+
                 |
                 v
          Streamlit UI
```
# Images
<img width="705" height="322" alt="Screenshot 2026-08-25 123123" src="https://github.com/user-attachments/assets/d6aaf784-4d30-40f5-84d7-628d61a5d47c" />

<img width="724" height="402" alt="Screenshot 2026-08-25 123308" src="https://github.com/user-attachments/assets/d129a0af-fa29-4cd8-a102-f8a46f741b93" />
<img width="718" height="384" alt="Screenshot 2026-08-25 123317" src="https://github.com/user-attachments/assets/85d4e8e8-9fa7-4b4d-8a4d-4f19830cb489" />


