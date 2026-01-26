from fastapi import UploadFile, File, HTTPException, status
import os
import shutil
from core.config import UPLOAD_DIR, MetaFile


def load_pdf_to_disk(file: UploadFile = File(...)) -> MetaFile:

    # Checks if there is file really.
    if file is None or file.filename == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please choose a file."
        )
    # Checks if the file type is pdf.
    if not file.filename.lower().endswith("pdf"):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail= "Only pdf files accepted."
        )
    
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, 
            detail="Only pdf files accepted.")

    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb", encoding="utf-8") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occured. {str(e)}"
        )
    
    return {
        "file_name": file.filename,
        "content_type": file.content_type,
        "file_path": file_path,
        "detail": "File saved."
    }

def ingest_file(file: UploadFile = File(...)) -> str:

    load_pdf_to_disk(file)
