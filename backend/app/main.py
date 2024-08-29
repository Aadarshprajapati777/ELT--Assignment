from fastapi import FastAPI
from app.api.v1.endpoints import file_upload, dashboard

app = FastAPI()

app.include_router(file_upload.router, prefix="/api/v1")
