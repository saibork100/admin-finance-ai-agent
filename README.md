<div align="center">

# 🤖 Admin & Finance AI Agent

### An autonomous LLM-powered agent for administrative and financial task management

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.2-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)](https://langchain.com)
[![LlamaIndex](https://img.shields.io/badge/LlamaIndex-0.10-FF6B35?style=for-the-badge)](https://llamaindex.ai)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

[Features](#-features) · [Architecture](#-architecture) · [Quick Start](#-quick-start) · [API Docs](#-api-reference) · [Demo](#-demo)

</div>

---

## 📌 Overview

This project is an **autonomous AI agent** that handles administrative and financial queries for small to medium businesses. It combines **LLM reasoning** (via LangChain tool-calling), **document retrieval** (LlamaIndex RAG pipeline), and a **FastAPI REST interface** to automate real business workflows — from answering invoice questions to generating financial summaries.

Built as a final-year dissertation project at the University of Westminster.

---

## ✨ Features

- 🧠 **Autonomous reasoning** — LangChain agent decides which tools to invoke based on the user's query, no hardcoded logic
- 📄 **Document Q&A** — Ask questions about invoices, contracts, and reports using LlamaIndex RAG with persistent vector store
- 💰 **Financial summaries** — Automatically generates income/expense summaries from uploaded CSV data
- 📅 **Task routing** — Routes admin tasks (meeting scheduling, email drafting) to the appropriate tool or API
- 🔐 **Secure API** — JWT-authenticated REST endpoints via FastAPI
- 🐳 **Containerised** — Docker Compose setup for one-command deployment
- 🔁 **n8n integration** — Webhook triggers connect the agent to external automation workflows

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Client / n8n                      │
│              (REST API · Webhooks)                   │
└───────────────────────┬─────────────────────────────┘
                        │ HTTP / JWT
┌───────────────────────▼─────────────────────────────┐
│                  FastAPI Gateway                     │
│         (Auth · Rate limiting · Routing)             │
└──────────┬────────────────────────┬─────────────────┘
           │                        │
┌──────────▼──────────┐   ┌─────────▼────────────────┐
│   LangChain Agent   │   │    LlamaIndex RAG Engine  │
│  (Tool orchestrator)│   │  (Document Q&A · Vector   │
│                     │   │   Store · Embeddings)     │
└──────────┬──────────┘   └─────────────────────────┘
           │
    ┌──────┴───────┐
    │    Tools     │
    ├──────────────┤
    │ • Finance    │  ← CSV parser, expense calculator
    │ • Docs       │  ← Invoice reader, contract search
    │ • Calendar   │  ← Meeting scheduler
    │ • Email      │  ← Draft generation
    └──────────────┘
```

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Agent Framework | LangChain (tool-calling agent) |
| Document Retrieval | LlamaIndex + ChromaDB vector store |
| LLM | OpenAI GPT-4o / GPT-4o-mini |
| API | FastAPI + Pydantic v2 |
| Auth | JWT (python-jose) |
| Automation | n8n (self-hosted) |
| Infrastructure | Docker · Docker Compose |
| CI/CD | GitHub Actions |
| Language | Python 3.11 · TypeScript 5 |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- OpenAI API key

### 1. Clone the repository
```bash
git clone https://github.com/saibork100/admin-finance-ai-agent.git
cd admin-finance-ai-agent
```

### 2. Set up environment variables
```bash
cp .env.example .env
# Add your OPENAI_API_KEY and JWT_SECRET to .env
```

### 3. Run with Docker
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

### 4. Run locally (without Docker)
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 📡 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/token` | Get JWT access token |
| `POST` | `/agent/query` | Send a query to the AI agent |
| `POST` | `/documents/upload` | Upload PDF/CSV for RAG indexing |
| `GET` | `/finance/summary` | Get financial summary report |
| `GET` | `/health` | Health check |

Interactive docs available at `http://localhost:8000/docs` (Swagger UI).

**Example request:**
```bash
curl -X POST http://localhost:8000/agent/query \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"query": "Summarise all outstanding invoices from Q1 2025"}'
```

**Example response:**
```json
{
  "answer": "You have 3 outstanding invoices from Q1 2025 totalling £12,450. The oldest is Invoice #INV-0042 from January 14th...",
  "sources": ["invoices_q1_2025.pdf"],
  "tools_used": ["document_search", "finance_calculator"],
  "tokens_used": 847
}
```

---

## 🎬 Demo

> *Screenshots and demo video coming soon.*

| Query | Agent Response |
|-------|---------------|
| "What are my total expenses for March?" | Parses uploaded CSV, calculates and returns categorised summary |
| "Draft an email to chase Invoice #42" | Generates professional follow-up email draft |
| "What does clause 7 of the contract say?" | Performs semantic search over uploaded contract PDF |

---

## 📁 Project Structure

```
admin-finance-ai-agent/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── agent/
│   │   ├── agent.py         # LangChain agent setup
│   │   └── tools/           # Custom tools (finance, docs, calendar)
│   ├── rag/
│   │   ├── indexer.py       # LlamaIndex document ingestion
│   │   └── retriever.py     # Query engine
│   ├── api/
│   │   ├── routes/          # API route handlers
│   │   └── auth.py          # JWT authentication
│   └── models/              # Pydantic schemas
├── tests/                   # pytest unit & integration tests
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

---

## 🧪 Running Tests

```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

---

## 🗺 Roadmap

- [x] Core LangChain agent with tool-calling
- [x] LlamaIndex RAG pipeline
- [x] FastAPI REST interface with JWT auth
- [x] Docker containerisation
- [ ] Multi-tenant support
- [ ] Streaming responses (Server-Sent Events)
- [ ] Web UI (React dashboard)
- [ ] Support for local LLMs (Ollama)

---

## 👤 Author

**Mahmoud Triki**
- GitHub: [@saibork100](https://github.com/saibork100)
- LinkedIn: [linkedin.com/in/mahmoud-triki-002a02331](https://linkedin.com/in/mahmoud-triki-002a02331)
- Email: trikimahmoud86@gmail.com

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
