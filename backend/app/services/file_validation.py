import pandas as pd
from app.core.exceptions import FileValidationError
from app.core.logger import logger

def validate_file_extension(filename: str):
    logger.info("Inside file validation")
    if not (filename.endswith('.csv') or filename.endswith('.xlsx')):
        raise FileValidationError()
