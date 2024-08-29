import pandas as pd
from app.core.logger import logger
from io import BytesIO

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