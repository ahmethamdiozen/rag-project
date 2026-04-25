import os
import sys
from unittest.mock import MagicMock, patch

# Set required env vars before any app imports
os.environ.setdefault("OPENAI_API_KEY", "sk-test-fake-key")

# Patch heavy external clients before app modules are loaded
_chroma_mock = MagicMock()
_chroma_mock.get_or_create_collection.return_value = MagicMock()
_chroma_mock.heartbeat.return_value = True

patch("chromadb.PersistentClient", return_value=_chroma_mock).start()
patch("openai.OpenAI", return_value=MagicMock()).start()

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)
