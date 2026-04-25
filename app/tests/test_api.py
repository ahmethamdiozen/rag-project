import io
from unittest.mock import patch


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_files_empty(client, tmp_path, monkeypatch):
    monkeypatch.setattr("app.api.routes.UPLOAD_DIR", tmp_path)
    response = client.get("/files")
    assert response.status_code == 200
    assert response.json() == []


def test_list_files_returns_pdfs(client, tmp_path, monkeypatch):
    monkeypatch.setattr("app.api.routes.UPLOAD_DIR", tmp_path)
    (tmp_path / "doc.pdf").write_bytes(b"fake")
    (tmp_path / "notes.txt").write_bytes(b"fake")
    response = client.get("/files")
    assert response.status_code == 200
    assert response.json() == ["doc.pdf"]


def test_upload_requires_pdf(client):
    data = {"file": ("notes.txt", io.BytesIO(b"hello"), "text/plain")}
    response = client.post("/upload", files=data)
    assert response.status_code == 415


def test_upload_too_large(client):
    big = io.BytesIO(b"a" * (11 * 1024 * 1024))
    data = {"file": ("big.pdf", big, "application/pdf")}
    response = client.post("/upload", files=data)
    assert response.status_code == 413


def test_ask_missing_question(client):
    response = client.post("/ask", json={})
    assert response.status_code == 422


def test_ask_returns_answer(client):
    mock_result = {"answer": "test answer", "sources": []}
    with patch("app.api.routes.answer_question", return_value=mock_result):
        response = client.post("/ask", json={"question": "What is this?"})
    assert response.status_code == 200
    assert response.json()["answer"] == "test answer"
