[🇬🇧 English](README.EN.md)

# RAG Doküman Soru-Cevap — Backend

PDF yükle, doğal dilde soru sor — cevaplar kaynak materyale dayandırılır ve sayfa düzeyinde atıflarla desteklenir. Yüksek seviyeli framework kullanılmadan sıfırdan yazılmış RAG pipeline.

**Canlı demo:** [rag.ahmethamdiozen.site](https://rag.ahmethamdiozen.site) · **Frontend repo:** [rag-frontend](https://github.com/ahmethamdiozen/rag-frontend)

---

## Nasıl çalışır

```
PDF Yükleme → Disk + Tekrar yükleme kontrolü → Metin çıkarımı (sayfa bazında)
           → Parçalama (600 token, 100 token örtüşme)
           → OpenAI embedding → ChromaDB
           → Anlamsal sorgulama → LLM cevabı + kaynak atıfları
```

Kaynaklar gösterilmeden önce cevabın gerçekten getirilen chunk'larla desteklendiği ikinci bir LLM çağrısıyla doğrulanır — desteklenmiyorsa kaynaklar gösterilmez (halüsinasyon önleme).

---

## Teknoloji Yığını

| Katman | Teknoloji |
|---|---|
| API | FastAPI, Uvicorn |
| Embedding | OpenAI `text-embedding-3-small` |
| Vektör deposu | ChromaDB (kalıcı) |
| PDF ayrıştırma | pypdf |
| Doğrulama | Pydantic v2 |

---

## API Uç Noktaları

| Metod | Yol | Açıklama |
|---|---|---|
| `POST` | `/upload` | PDF yükle (maks 10 MB) |
| `POST` | `/ask` | Soru sor, isteğe bağlı dosya filtresi |
| `GET` | `/files` | İndekslenmiş dokümanları listele |
| `GET` | `/health` | Sağlık kontrolü (ChromaDB ping) |

**POST /ask** gövdesi:
```json
{
  "question": "Temel bulgular nelerdir?",
  "files": ["rapor.pdf"]
}
```

---

## Yerel Kurulum

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-..." > .env
uvicorn app.main:app --reload
```

---

## Docker

```bash
docker build -t rag-backend .
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-... rag-backend
```

Kalıcı depolama ile production için:
```bash
docker compose -f docker-compose.prod.yaml up
```

---

## Testler

```bash
pip install -r requirements-dev.txt
pytest app/tests/ -v
```

---

## Ortam Değişkenleri

| Değişken | Zorunlu | Açıklama |
|---|---|---|
| `OPENAI_API_KEY` | Evet | OpenAI API anahtarı |
| `ALLOWED_ORIGINS` | Hayır | Virgülle ayrılmış CORS kaynakları (varsayılan: `http://localhost:3000`) |
