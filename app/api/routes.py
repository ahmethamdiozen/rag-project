from fastapi import APIRouter, UploadFile, File
from services.ingestion import ingest_file
from core.config import MetaFile


router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    ingest_file(file)


    return {}