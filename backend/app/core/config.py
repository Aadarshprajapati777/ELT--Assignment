import os

class Settings:
    PROJECT_NAME: str = "ELT System"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
    ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
    EACH_FILE_SIZE = 2 * 1024 * 1024  # 2 MB in bytes

settings = Settings()