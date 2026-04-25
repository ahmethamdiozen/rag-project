from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.services.ingestion import ingest_file
from app.services.query import answer_question, generate_stream
from app.core.config import Request, UPLOAD_DIR, chroma_client

MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if file.size and file.size > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10 MB.")

    result = await ingest_file(file)
    return result

@router.post("/ask")
async def ask(payload: Request):
    if payload.files:
        file_names = [f.strip().lower() for f in payload.files]
        return answer_question(question=payload.question, n_results=payload.n_results, file_names=file_names)
    return answer_question(question=payload.question, n_results=payload.n_results)

@router.get("/files")
async def list_files():
    files = []
    for file in UPLOAD_DIR.iterdir():
        if file.is_file() and file.suffix.lower() == ".pdf":
            files.append(file.name)
    return files

@router.post("/ask/stream")
def ask_stream(payload: Request):
    file_names = [f.strip().lower() for f in payload.files] if payload.files else None
    return StreamingResponse(
        generate_stream(question=payload.question, n_results=payload.n_results, file_names=file_names),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.get("/health")
async def health():
    try:
        chroma_client.heartbeat()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"ChromaDB unavailable: {e}")
    return {"status": "ok"}