import pandas as pd
from app.core.exceptions import FileValidationError
from app.core.logger import logger
from io import BytesIO

def validate_file_extension(filename: str):
    logger.info("Inside file validation")
    if not (filename.endswith('.csv') or filename.endswith('.xlsx')):
        raise FileValidationError()

def read_file(file, filename: str):
    logger.info("Inside read file")
    
    if file is None:
        raise ValueError("File object is None")
    
    file.seek(0)
    
    logger.info(f"Reading file with name: {filename}")
    
    if filename.endswith('.csv'):
        return pd.read_csv(file)
    elif filename.endswith('.xlsx'):
        return pd.read_excel(BytesIO(file.read()))
    else:
        raise ValueError("Unsupported file format")
