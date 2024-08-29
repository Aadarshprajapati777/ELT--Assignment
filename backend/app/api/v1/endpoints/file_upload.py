from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import List
from app.services.file_service import validate_file_extension, read_file
from app.core.logger import logger

router = APIRouter()

@router.get("/upload")
async def file_upload():
    return {"message": "in file_upload file"}

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    processed_files = []
    for file in files:
        try:
            validate_file_extension(file.filename)
            df = read_file(file.file, file.filename)
            logger.info(f"Processed file: {file.filename}")
            processed_files.append(file.filename)
        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing file {file.filename}: {str(e)}")

    return {"message": f"Successfully processed files: {processed_files}"}
