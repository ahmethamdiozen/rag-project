# RAG Project (+ rag_frontend) — Deployment Roadmap

**Target subdomain**: `rag.ahmethamdiozen.com`
**Deploy order in pipeline**: 2nd (after clinic-appointment)
**Scope**: `rag_project/` (FastAPI backend: OpenAI embeddings + ChromaDB + pypdf) **paired with** `rag_frontend/` (Next.js frontend). Deployed together as one app behind a single subdomain.

**Status**: clean modular FastAPI backend exists; frontend is a `create-next-app` scaffold — wiring + UI work needed. Best candidate for the "lightweight, cloud-first RAG" slot in the portfolio (distinct from the heavier `rag-mvp` which stays as a GitHub-only offline demo).

**Note on `rag-mvp`**: NOT deployed. Kept as pinned GitHub repo with a video demo to showcase the **offline/air-gapped** angle (Ollama + Llama 3 8B). Portfolio card links to the video, not to a live URL.

---

## North Star

A cloud-hosted "internal document Q&A" demo. Visitor lands on `rag.ahmethamdiozen.com`, uploads a PDF (or picks from seeded samples), asks a question, gets a grounded answer with **source citations (file + page)**. This is the lightweight, cloud-first RAG — complements `hf-saas` (which is the SaaS framework around RAG) and `rag-mvp` (which is the offline/local version, video-only).

---

## Phase 0 — Deploy Blockers

### Backend (`rag_project/`)

- [ ] **Env validation on startup** — `app/core/config.py` must require `OPENAI_API_KEY` (no default). Fail fast on missing.
- [ ] **CORS allowlist** — add FastAPI CORS middleware restricting to `rag.ahmethamdiozen.com` in prod.
- [ ] **Upload size + type guard** — `POST /upload` currently accepts any PDF. Add max 10 MB, `application/pdf` only, filename sanitization.
- [ ] **Persistent ChromaDB volume** — today `data/chroma/` is local. In Coolify, mount a persistent volume at `/app/data` so indexes survive restarts.
- [ ] **`/health` endpoint** — ping OpenAI credential validity (or skip if too noisy), verify ChromaDB accessible, DB if any.
- [ ] **Add `Dockerfile`** (currently only `requirements.txt` + raw uvicorn). Multi-stage: install deps, copy app, non-root, `uvicorn app.main:app --host 0.0.0.0 --port 8000`.
- [ ] **Write `docker-compose.prod.yaml`** tying backend + frontend together.

### Frontend (`rag_frontend/`)

- [ ] **Wire to backend API** — today frontend is a Next.js bootstrap with no API calls. Build:
  - Upload page: file picker → `POST /upload` with progress
  - Chat page: input + message list, calls `POST /ask?question=...`
  - Source citations render: if backend returns sources, show each with "open PDF at page N" link
- [ ] **Environment config** — `NEXT_PUBLIC_API_URL=https://rag.ahmethamdiozen.com/api`.
- [ ] **Dockerfile** for Next.js — multi-stage, `next build`, `next start` or static export.
- [ ] **Delete Vercel boilerplate text** from `README.md`.

### Cost control

- [ ] **OpenAI rate limit on `/ask`** — per-IP 10 queries/minute, per-IP 100/day. Redis-backed counter. Protects from quota exhaustion by bad actors.
- [ ] **Embedding cost estimator** — on upload, before embedding, estimate token count and reject if > $0.50. Show cost to user.
- [ ] **Daily spend cap** — env var `DAILY_BUDGET_USD=2.00`. Middleware tracks Redis counter; when exceeded, return 503 with friendly message. Reset at 00:00 UTC.

### Security

- [ ] **No open upload in prod** — require a simple magic link or per-IP quota. A viral HackerNews post could drain the OpenAI budget in minutes.

### Deploy wiring

- [ ] **Reverse-proxy path layout** — frontend at `/`, backend at `/api/*` (rewrite in Next.js or in Coolify's Traefik config).
- [ ] **Two Coolify services** — backend (FastAPI container) and frontend (Next.js container or static build).

### Demo data

- [ ] **Pre-seed 3 sample PDFs** — an HR policy (redacted), a research paper abstract compilation, a user manual. Users can pick these if they don't want to upload their own.
- [ ] **Suggested questions for each sample** — buttons that pre-fill the input.

---

## Phase 1 — Post-Deploy MVP Gaps

### Retrieval quality

- [ ] **Source citations in answers** — README already lists this as a possible extension. Modify the RAG pipeline (`app/services/rag.py`) to return `{ answer, sources: [{ filename, page, chunk_text }] }`. Render in frontend.
- [ ] **Chunk overlap** — current chunking is fixed-size; add overlap (e.g., 200-token overlap on 1000-token chunks) to reduce cut-off context.
- [ ] **Metadata filtering** — README lists as extension. Scope queries to specific uploaded files via frontend UI dropdown.
- [ ] **Reranker layer** — after Chroma top-k retrieval, rerank top 20 with a cheap cross-encoder (or Cohere rerank) → keep top 5 for LLM context.
- [ ] **Empty-retrieval handling** — if no chunks score above threshold, answer "I don't have information about that in the uploaded documents" instead of hallucinating.

### UX polish

- [ ] **Streaming responses** — SSE from backend, token-by-token display in frontend.
- [ ] **Upload progress + indexing progress** — spinner + "chunked 42 pages, embedding..." status during ingestion.
- [ ] **Conversation history** — sidebar with prior Q&A threads; stored in localStorage first, later in DB if auth added.
- [ ] **Drag-and-drop upload** instead of click-to-select.

### Backend robustness

- [ ] **Error responses are structured** — `{ error: "code", message: "human-readable" }` shape, not raw Python tracebacks.
- [ ] **Retry on OpenAI 429** — exponential backoff, max 3 retries.
- [ ] **Background task queue** — today `/upload` is synchronous (blocking). For larger PDFs, move to a background task (FastAPI BackgroundTasks or Celery/RQ). Respond with `202 Accepted + jobId`; frontend polls.

### Observability

- [ ] **Log every query** — sanitized (no PII), with timing + tokens used + cost estimate. Append to a log file + Sentry on error.
- [ ] **`/metrics` Prometheus endpoint** — optional if Grafana dashboard wanted across projects.

---

## Phase 2 — Polish / Portfolio Readiness

- [ ] **Screenshot pack** — landing, upload flow, chat with citation-rich answer, sample PDF view.
- [ ] **60s video demo** — upload PDF, ask 3 questions, show cited answers.
- [ ] **Portfolio card on ahmethamdiozen.com**:
  - Title: "RAG Document QA (cloud)"
  - Tech: FastAPI, OpenAI embeddings + chat, ChromaDB, Next.js
  - Links: live demo, GitHub, video
  - TR + EN
  - **Link to `rag-mvp` nearby**: "Same project but fully offline → [video of offline version]"
- [ ] **Blog-style `/about` page** explaining: "why source citations matter", "chunk overlap tradeoffs", "cost control strategy".
- [ ] **Landing page** — not dumped into the chat UI; a proper hero + "try it" button.

### CI/CD

- [ ] **GitHub Actions**: `ruff` + `mypy` + `pytest` backend, `eslint` + `next build` frontend. Coolify webhook on main.
- [ ] **Smoke test on deploy** — hit `/api/health` and `/` — fail deploy if either doesn't 200.

---

## Phase 3 — Stretch

- [ ] **Auth system** — GitHub OAuth login so users have their own doc workspace (eliminates the need for strict per-IP limits).
- [ ] **Persistent conversation history in DB** (Postgres) tied to user account.
- [ ] **Multi-modal inputs** — accept DOCX, TXT, MD in addition to PDF. Later: image OCR.
- [ ] **Alternative LLM backends** — toggleable: OpenAI / Claude / local Ollama (ties back to `rag-mvp` infrastructure).
- [ ] **Fine-grained embedding model choice** — let user pick MiniLM (free) or OpenAI (better).
- [ ] **Export answer as Markdown/PDF** for sharing.
- [ ] **Team workspaces** — align with hf-saas' team model if keeping them separate makes less sense long-term.

---

## Deploy Checklist (Coolify)

1. DNS: A record for `rag.ahmethamdiozen.com`.
2. Coolify Redis resource (for rate-limit counters).
3. Backend service: `rag_project/Dockerfile`, port 8000, env `OPENAI_API_KEY`, `CHROMA_DB_PATH=/app/data/chroma`, persistent volume at `/app/data`.
4. Frontend service: `rag_frontend/Dockerfile`, `NEXT_PUBLIC_API_URL=https://rag.ahmethamdiozen.com/api`.
5. Reverse proxy: `/` → frontend, `/api/*` → backend.
6. Domain + Let's Encrypt SSL.
7. Copy pre-seeded PDFs into persistent volume once.
8. Smoke test: load page, upload sample PDF, ask a question, see cited answer.

---

## Demo Setup

- Landing at `rag.ahmethamdiozen.com`.
- 3 pre-seeded sample PDFs with suggested questions.
- Users can upload their own (subject to per-IP quota + daily budget cap).
- README prominently links to `rag-mvp` video for the "fully offline" variant.
