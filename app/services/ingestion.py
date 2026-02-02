from fastapi import UploadFile, File, HTTPException, status
import shutil
from app.core.config import MetaFile, PageText, ChunkText
from pypdf import PdfReader
from app.core.config import UPLOAD_DIR
import re
from app.services.embedding import embed_texts
from app.services.vectorstore import save_to_chroma
import hashlib
from pathlib import Path
from app.core.config import collection

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
        file_name=file.filename,
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
    texts: list[PageText] = []

    for i, page in enumerate(reader.pages):
        raw_text = page.extract_text()
        if not raw_text:
            continue

        cleaned_text = clean_text(raw_text)
        if not cleaned_text:
            continue

        texts.append(PageText(
            page=i+1,
            text=cleaned_text,
            file_name=file_info.file_name
        ))

    return texts

def chunk_text(text: str, chunk_len: int = 600, overlap_len = 100) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_len
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap_len

    return chunks

def compute_file_hash(file_path: Path) -> str:
    hasher = hashlib.sha256()

    with  file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            hasher.update(chunk)

    return hasher.hexdigest()

def is_file_already_ingested(file_hash: str) -> bool:
    result = collection.get(
        where={"file_hash": file_hash},
        limit=1
    )
    return len(result["ids"]) > 0

def page_to_chunk(pages: list[PageText]) -> list[ChunkText]:

    if not pages:
        return []
    
    file_name = pages[0].file_name
    chunks: list[ChunkText] = []

    for page in pages:
        page_chunks = chunk_text(page.text)

        for chunk in page_chunks:
            chunks.append(
                ChunkText(
                    text=chunk,
                    page=page.page,
                    file_name=file_name
                )
            )
    
    return chunks

async def ingest_file(file: UploadFile = File(...)):

    meta = await load_pdf_to_disk(file)
    file_hash = compute_file_hash(meta.file_path)

    if is_file_already_ingested(file_hash):
        return {
            "status": "skipped",
            "message": "File already ingested."
        }
    
    pages = pdf_to_text(meta)
    chunks = page_to_chunk(pages)

    if not chunks:
        return {
            "status": "skipped",
            "message": "No text chunks extracted"
        }

    texts = [c.text for c in chunks]

    metadatas = [
        {
        "file_name": meta.file_name,
        "page": c.page,
        "file_hash": file_hash
    } for c in chunks
    ]

    embeddings = embed_texts(texts=texts)

    save_to_chroma(
        texts=texts, 
        embeddings=embeddings, 
        metadatas=metadatas
    )

    return {
        "status": "ingested",
        "chunks": len(chunks)}