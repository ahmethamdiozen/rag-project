from fastapi import APIRouter, UploadFile, File, Body
from app.services.ingestion import ingest_file
from app.services.query import answer_question
from app.core.config import Request

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    text = await ingest_file(file)


    return {"text": text}

@router.post("/ask")
async def ask(payload: Request):

    if payload.files:
        file_names = [f.strip().lower() for f in payload.files]
        return answer_question(question=payload.question, n_results=payload.n_results, file_names=file_names)
    return answer_question(question=payload.question, n_results=payload.n_results)