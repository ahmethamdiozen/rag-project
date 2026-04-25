# RAG Document Q&A — Backend

FastAPI backend for a cloud-hosted document question-answering system. Upload PDFs, ask natural-language questions, get answers grounded in the source material with page-level citations.

**Live demo:** [rag.ahmethamdiozen.site](https://rag.ahmethamdiozen.site) · **Frontend repo:** [rag-frontend](https://github.com/ahmethamdiozen/rag-frontend)

---

## How it works

```
PDF Upload → Disk + Dedup check → Text extraction (page-aware)
         → Chunking (600 tokens, 100-token overlap)
         → OpenAI embeddings → ChromaDB
         → Semantic retrieval → LLM answer + source citations
```

Answers are grounded-checked against retrieved context before sources are returned — if the answer isn't supported by the chunks, sources are omitted.

---

## Stack

| Layer | Tech |
|---|---|
| API | FastAPI, Uvicorn |
| Embeddings | OpenAI `text-embedding-3-small` |
| Vector store | ChromaDB (persistent) |
| PDF parsing | pypdf |
| Validation | Pydantic v2 |

---

## API

| Method | Path | Description |
|---|---|---|
| `POST` | `/upload` | Upload a PDF (max 10 MB) |
| `POST` | `/ask` | Ask a question, optionally filter by files |
| `GET` | `/files` | List indexed documents |
| `GET` | `/health` | Health check (ChromaDB ping) |

**POST /ask** body:
```json
{
  "question": "What are the key findings?",
  "files": ["report.pdf"]
}
```

---

## Local setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-..." > .env
uvicorn app.main:app --reload
```

---

## Docker

```bash
docker build -t rag-backend .
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-... rag-backend
```

For production with persistent storage:
```bash
docker compose -f docker-compose.prod.yaml up
```

---

## Tests

```bash
pip install -r requirements-dev.txt
pytest app/tests/ -v
```

---

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `ALLOWED_ORIGINS` | No | Comma-separated CORS origins (default: `http://localhost:3000`) |
