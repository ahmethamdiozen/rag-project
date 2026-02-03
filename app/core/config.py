from dotenv import load_dotenv
import os
from pathlib import Path
from pydantic import BaseModel
from openai import OpenAI
import chromadb
load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR = BASE_DIR / "data" / "chroma"
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
openai_client = OpenAI(api_key=OPENAI_API_KEY)
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = chroma_client.get_or_create_collection(name="Docs")

class MetaFile(BaseModel):
    file_name: str
    content_type: str
    file_path: Path
    detail: str = "None"

    model_config = {"arbitrary_types_allowed": "True"}

class PageText(BaseModel):
    page: int
    text: str
    file_name: str

class ChunkText(BaseModel):
    page: int
    text: str
    file_name: str

class Request(BaseModel):
    question: str
    n_results: int = 5
    files: list[str] | None = None