from fastapi import UploadFile, File, HTTPException, status
import os
import shutil
from app.core.config import MetaFile, PageText
from pypdf import PdfReader
from pathlib import Path
from app.core.config import UPLOAD_DIR
import re


async def load_pdf_to_disk(file: UploadFile) -> MetaFile:

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
        path = UPLOAD_DIR / file.filename

        with path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occured. {str(e)}"
        )
    
    return MetaFile(
        file_name= file.filename,
        content_type=file.content_type,
        file_path=path,
        detail="file saved."
    )


def clean_text(raw_text: str) -> str:

    text = raw_text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()

    return text


def pdf_to_text(file_info: MetaFile) -> list[PageText]:

    reader = PdfReader(str(file_info.file_path))
    pages: list[PageText] = []

    for i, page in enumerate(reader.pages):
        raw_text = page.extract_text()
        if not raw_text:
            continue

        cleaned_text = clean_text(raw_text)
        if not cleaned_text:
            continue

        pages.append(PageText(
            page= i+1,
            text=cleaned_text
        ))

    return pages

async def ingest_file(file: UploadFile = File(...)) -> str:

    meta = await load_pdf_to_disk(file)
    text = pdf_to_text(meta)
    print("......", text)

    return text[1].text