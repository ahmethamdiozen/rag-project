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
async def ask(question: str):
    answer = answer_question(question=question)
    print("ANSWER IN ENDPOINT:", answer, type(answer))
    return {"answer": answer}

