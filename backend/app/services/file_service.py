import pandas as pd
from app.core.exceptions import FileValidationError

#checking file type and reading files

def validate_file_extension(filename: str):
    if not (filename.endswith('.csv') or filename.endswith('.xlsx')):
        raise FileValidationError()

def read_file(file_path: str):
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    else:
        raise FileValidationError()
