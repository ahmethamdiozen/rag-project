from fastapi import APIRouter, UploadFile, File
from app.services.ingestion import ingest_file
from app.services.query import answer_question
from app.core.config import MetaFile

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    text = await ingest_file(file)


    return {"text": text}

@router.post("/ask")
async def ask(question: str, n_results, file_name: str | None = None):

    return answer_question(question=question, n_results=n_results, file_name=file_name)