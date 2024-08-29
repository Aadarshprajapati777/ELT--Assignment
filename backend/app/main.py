from fastapi import FastAPI
from app.api.v1.endpoints import file_upload, dashboard

# Create FastAPI instance
app = FastAPI()

# Include routers for the endpoints
app.include_router(file_upload.router, prefix="/api/v1")
