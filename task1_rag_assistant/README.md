# Task 1 – RAG AI Assistant

For this task, I built a simple RAG-based AI assistant using FastAPI, Gemini, ChromaDB, and Docker.

The main goal was to allow a user to upload a document, store its information in a vector database, and then ask questions based on the uploaded content.

## What I implemented

The assistant supports:

- PDF and TXT document upload
- Text extraction
- Text chunking
- Gemini embeddings
- ChromaDB vector storage
- Retrieval of relevant document chunks
- Gemini for answer generation
- Structured JSON responses
- Tool/function calling
- Calculator tool
- Docker support
- Local open-source model serving with vLLM

## How the RAG system works

When a document is uploaded, the text is first extracted and divided into smaller chunks.

Each chunk is converted into an embedding using the Gemini embedding model and then stored in ChromaDB together with its metadata.

When the user asks a question, the question is also converted into an embedding. ChromaDB is then searched to find the most relevant chunks.

Those retrieved chunks are added to the prompt as context before the question is sent to the LLM.

The basic flow is:


Document
   ↓
Text Extraction
   ↓
Chunking
   ↓
Gemini Embeddings
   ↓
ChromaDB