# Week 15 Assignment – RAG Assistant and Model Productionization

This assignment contains two parts. In Task 1, I built a RAG-based AI assistant. In Task 2, I productionized the customer-support routing model that I trained during Week 14.

Both tasks are containerized and can be run using Docker.

---

## Task 1 – RAG AI Assistant

For Task 1, I built an AI assistant that can answer questions using information from uploaded documents.

The application supports PDF, TXT, and Markdown documents.

The main flow is:

1. Upload a document.
2. Extract the text from the document.
3. Split the text into smaller overlapping chunks.
4. Generate embeddings using Gemini embeddings.
5. Store the embeddings and document metadata in ChromaDB.
6. Convert the user's question into an embedding.
7. Retrieve the most relevant chunks from ChromaDB.
8. Add the retrieved information to the prompt.
9. Send the prompt to Gemini.
10. Return a structured JSON response with the answer and sources.

The main cloud LLM used for this task is Gemini.

The embedding model used is:

`gemini-embedding-001`

The vector database used is:

`ChromaDB`

Task 1 also includes function/tool calling. I implemented a calculator tool and tested it successfully.

For example:

`Calculate 25 * 16.`

returned:

`25 * 16 = 400`

I also tested local open-source model serving using vLLM on a Google Colab T4 GPU.

The local model used was:

`Qwen/Qwen3-0.6B`

The vLLM server successfully returned HTTP status 200 and generated a response through its OpenAI-compatible API.

Task 1 source code is located in:

`task1_rag_assistant/`

---

## Task 2 – Productionized Week 14 Router

For Task 2, I reused the DistilBERT customer-support routing model that I trained during Week 14.

The trained model is included in:

`task2_production_router/model/week14_distilbert_router/`

The model classifies customer messages into 11 support categories:

- ACCOUNT
- CANCEL
- CONTACT
- DELIVERY
- FEEDBACK
- INVOICE
- ORDER
- PAYMENT
- REFUND
- SHIPPING
- SUBSCRIPTION

I connected the model to a FastAPI backend and a Streamlit frontend.

The production application includes:

- Single-message prediction
- Batch prediction
- Confidence scores
- Human-review flag
- Asynchronous request handling
- Concurrency control
- Rate limiting
- Input validation
- Retry and fallback logic
- Graceful degradation
- Docker containerization
- Performance benchmarking

For example, I tested the message:

`My card payment keeps getting declined.`

The model returned:

`PAYMENT`

with approximately 99.8% confidence.

I also tested batch prediction using payment, subscription, and refund messages, and the API returned the correct routing categories.

Task 2 source code is located in:

`task2_production_router/`

---

## Performance Benchmark

I benchmarked the Task 2 router using 50 requests and 4 concurrent workers.

The results were:

| Metric | Result |
|---|---:|
| Requests | 50 |
| Concurrent Workers | 4 |
| Mean Latency | 33.02 ms |
| Median Latency | 6.17 ms |
| p95 Latency | 224.41 ms |
| Throughput | 117.78 requests/second |

These results were measured while running the DistilBERT router locally.

This assignment helped me work with both RAG systems and model deployment.

In Task 1, I implemented document ingestion, chunking, Gemini embeddings, ChromaDB retrieval, structured responses, function calling, Docker, and local model serving using vLLM.

In Task 2, I took my Week 14 DistilBERT model and turned it into a small production-style application using FastAPI and Streamlit. I also added batch inference, concurrency handling, rate limiting, fallback handling, Docker, and performance benchmarking.