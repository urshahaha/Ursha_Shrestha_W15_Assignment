# Task 2 – Productionized Week 14 Support Router

For this task, I productionized the customer-support routing model that I trained in Week 14.

The Week 14 model is a DistilBERT sequence-classification model. Instead of using the model only inside a notebook, I connected it to a FastAPI backend and a Streamlit frontend so that it can be used like a small production application.

---

## Model Used

The model used in this task is the DistilBERT classifier trained during Week 14.

It classifies customer-support messages into 11 categories:

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

The trained model files are stored in:

`task2_production_router/model/week14_distilbert_router/`

The folder contains the model weights, configuration, and tokenizer files required to load the model.

---

## What I Implemented

The production application includes:

- FastAPI backend
- Streamlit frontend
- Week 14 DistilBERT model
- Single-message prediction
- Batch prediction
- Confidence score
- Human-review flag
- Asynchronous request handling
- Concurrency control
- Rate limiting
- Input validation
- Retry and fallback logic
- Graceful degradation
- Docker containers
- Docker Compose
- Performance benchmarking

---

## How the System Works

The basic request flow is:

User
  ↓
Streamlit UI
  ↓
FastAPI Router API
  ↓
Rate Limiting + Input Validation
  ↓
Week 14 DistilBERT Router
  ↓
Predicted Support Category + Confidence
  ↓
Human Review Check
  ↓
Final API Response


In this task, I took the DistilBERT model from Week 14 and turned it into a small production-style AI service.

Instead of running predictions only from a notebook, the model can now be accessed through a FastAPI API and a Streamlit interface.

I also added batch prediction, asynchronous handling, concurrency control, rate limiting, input validation, fallback handling, Docker containerization, and performance benchmarking.