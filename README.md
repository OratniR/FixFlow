# FixFlow 🌊

**FixFlow** is a semantic knowledge base that transforms your debugging battles into reusable assets. It uses AI-driven **Vector Search** to help you find solutions based on the *meaning* of a problem, not just keywords.

![Architecture](./documents/architecture.md)

## 🚀 Features (MVP)

*   **Semantic Search**: Find "timeout issues" even if you search for "connection dropped".
*   **Knowledge Capture**: Structured format for Challenges, Solutions, and Tags.
*   **Local AI**: Runs 100% locally using `sentence-transformers` (no OpenAI key required).
*   **Scalable Storage**: Powered by **PostgreSQL** and **pgvector**.
*   **Modern UI**: Clean, responsive interface built with **Next.js 14**.

## 🛠️ Tech Stack

*   **Frontend**: Next.js 14 (TypeScript), Tailwind CSS
*   **Backend**: Python 3.11, FastAPI, Pydantic
*   **AI/ML**: `sentence-transformers` (all-MiniLM-L6-v2)
*   **Database**: PostgreSQL 15 + `pgvector` extension
*   **Infrastructure**: Docker Compose

## 🏁 Getting Started

### Prerequisites
*   Docker & Docker Compose

### Quick Start
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/fixflow.git
    cd fixflow
    ```

2.  **Start the stack**:
    ```bash
    docker-compose up -d --build
    ```

3.  **Access the application**:
    *   **Frontend**: [http://localhost:3000](http://localhost:3000)
    *   **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

### How to Use
1.  Open the App.
2.  Click **+ New Issue** to document a problem you just solved.
3.  Use the **Search Bar** to find it again using natural language (e.g., "How did I fix that database error?").

## 📂 Project Structure

```
├── backend/            # FastAPI Application
│   ├── app/
│   │   ├── api/        # API Routes
│   │   ├── services/   # Business Logic (Embeddings, Vector Store)
│   │   └── models.py   # Database Models
│   ├── Dockerfile
│   └── init.sql        # DB Init (Enable pgvector)
│
├── frontend/           # Next.js Application
│   ├── src/
│   │   ├── app/        # App Router Pages
│   │   ├── components/ # React Components
│   │   └── lib/        # API Client
│   └── Dockerfile
│
└── docker-compose.yml  # Orchestration
```

## 🔧 Configuration

Configuration is managed via environment variables. See `.env.example` in `backend/` and `frontend/`.

| Variable | Description | Default |
|----------|-------------|---------|
| `USE_LOCAL_EMBEDDING` | Use local CPU model vs OpenAI | `true` |
| `DATABASE_URL` | Postgres Connection String | `postgresql://...` |

## 🤝 Contributing

1.  Fork the repo.
2.  Create a branch (`git checkout -b feature/amazing-feature`).
3.  Commit your changes (`git commit -m 'Add amazing feature'`).
4.  Push to the branch (`git push origin feature/amazing-feature`).
5.  Open a Pull Request.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
