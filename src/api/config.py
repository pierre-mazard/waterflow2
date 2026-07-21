from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_URL: str
    OCR_API_KEY: str
    APP_ENV: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
