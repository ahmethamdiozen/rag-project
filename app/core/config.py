from dotenv import load_dotenv
import os
from pydantic import BaseModel
load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
UPLOAD_DIR = os.environ["UPLOAD_DIR"]


class MetaFile(BaseModel):
    file_name: str
    content_type: str
    file_path: str
    detail: str