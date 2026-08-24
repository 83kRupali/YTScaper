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
