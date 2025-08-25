from pathlib import Path
from pydantic import SecretStr
from pydantic import EmailStr 
from pydantic_settings import BaseSettings

ROOT = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # LLM / Portia
    GEMINI_API_KEY: SecretStr | None = None
    GEMINI_MODEL: str = "google/gemini-2.0-flash"
    PORTIA_API_KEY: SecretStr | None = None
    PORTIA_ENABLED: bool = False

    # Adzuna
    ADZUNA_APP_ID: str | None = None
    ADZUNA_APP_KEY: str | None = None
    ADZUNA_COUNTRY: str = "us"

    # Postmark
    POSTMARK_API_TOKEN: SecretStr | None = None
    POSTMARK_SENDER_EMAIL: EmailStr | None = None

    class Config:
        env_file = str(ROOT / ".env")
        env_file_encoding = "utf-8"

settings = Settings()
