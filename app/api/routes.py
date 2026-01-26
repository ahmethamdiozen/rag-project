from fastapi import APIRouter, UploadFile, File
from services.ingestion import load_pdf_to_disk
from core.config import MetaFile


router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file = load_pdf_to_disk(file)



    return {}