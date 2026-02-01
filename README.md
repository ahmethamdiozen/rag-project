# RAG-based Internal Document Question Answering System

This project is an internal **Retrieval-Augmented Generation (RAG)** system that enables semantic question answering over private PDF documents.  
It is designed as a **modular FastAPI backend application** suitable for internal knowledge management use cases.

---

## Features

- PDF document ingestion with validation and disk persistence  
- Page-aware text extraction and cleaning  
- Text chunking with metadata (file name, page number)  
- Embedding generation using OpenAI embedding models  
- Persistent vector storage using **ChromaDB**  
- Semantic similarity search over document chunks  
- Context-restricted LLM-based question answering  
- Modular and extensible service-oriented architecture  

---

## System Architecture

```text
PDF Upload
   ↓
Disk Persistence
   ↓
Text Extraction (page-based)
   ↓
Chunking + Metadata
   ↓
Embedding Generation
   ↓
Vector Database (Chroma)
   ↓
Semantic Retrieval
   ↓
LLM Answer Generation
```

The system ensures that LLM responses are **grounded strictly in retrieved document context**, reducing hallucinations.

---

## Tech Stack

- Python  
- FastAPI  
- OpenAI API (Embeddings & Chat Completions)  
- ChromaDB  
- pypdf  
- Git  

---

## Project Structure

```bash
app/
├── api/
│   └── routes.py          # API endpoints
├── services/
│   ├── ingestion.py       # File upload & PDF processing
│   ├── embedding.py       # Embedding generation
│   ├── vector_store.py    # ChromaDB operations
│   ├── rag.py             # Context building & LLM interaction
│   └── query.py           # End-to-end query pipeline
├── core/
│   └── config.py          # Settings & shared models
└── main.py
data/
├── uploads/               # Uploaded PDF files
└── chroma/                # ChromaDB files
```
---

## API Endpoints

### Upload PDF
```bash
POST /upload
```
Uploads a PDF file, stores it on disk, extracts text, and indexes it into the vector database.

---

### Ask a Question
```bash
POST /ask?question=...
```
Performs semantic search over indexed documents and returns an LLM-generated answer based on retrieved context.

---

## ⚙️ Setup & Run

### 1. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables
Create a **.env** file:

```bash
OPENAI_API_KEY=your_api_key_here
```

### 4. Run the application

```bash
uvicorn app.main:app --reload
```

## Design Notes

- The system does **not** rely on high-level frameworks like LangChain to maintain full control over the RAG pipeline.
- Embedding and query pipelines use the **same embedding model** to ensure vector consistency.
- Metadata (file name, page number) is preserved to support future features such as source attribution.

---

## Possible Extensions

- Source citation in answers (file name and page number)
- Metadata-based filtering (per document or department)
- Chunk overlap and adaptive chunk sizing
- Reranking retrieved chunks
- Authentication and access control for internal use

---

## License

This project is intended for educational and personal use.
