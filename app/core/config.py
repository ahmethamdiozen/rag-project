from dotenv import load_dotenv
import os
from pathlib import Path
from pydantic import BaseModel
load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
BASE_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class MetaFile(BaseModel):
    file_name: str
    content_type: str
    file_path: Path
    detail: str = "None"

    model_config = {"arbitrary_types_allowed": "True"}


class PageText(BaseModel):
    page: int
    text: str
