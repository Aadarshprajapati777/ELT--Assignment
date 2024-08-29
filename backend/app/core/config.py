import os

class Settings:
    PROJECT_NAME: str = "ELT System"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@db/dbname")
    ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

settings = Settings()
