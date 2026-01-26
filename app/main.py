from fastapi import FastAPI, UploadFile, HTTPException, File
from api.routes import router

app = FastAPI()

app.include_router(router)
