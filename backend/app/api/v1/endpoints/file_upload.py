from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from typing import List

from fastapi.responses import JSONResponse
from app.services.file_validation import validate_file_extension
from app.elt.extract import read_file
from app.core.logger import logger
from app.elt.load import load_data_to_database
from app.models.database import get_db
from sqlalchemy.orm import Session


router = APIRouter()

@router.get("/health")
async def health_check():
    return JSONResponse(status_code=200, content={"message": "API is healthy"})

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    processed_files = []
    for file in files:
        try:
            validate_file_extension(file.filename)

            #extract
            df = read_file(file.file, file.filename)
            logger.info(f"looking for type in df: {df.columns}")
            logger.info(f"Processed file: {file.filename}")
            processed_files.append(file.filename)

            #load
            load_data_to_database(df, db)

        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing file {file.filename}: {str(e)}")

    return {"message": f"Successfully processed files: {processed_files}"}
