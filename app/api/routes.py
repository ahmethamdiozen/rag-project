from fastapi import APIRouter, UploadFile, File
from app.services.ingestion import ingest_file
from app.core.config import MetaFile


router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    text = await ingest_file(file)


    return {"text": text}