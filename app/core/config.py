import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
APP_ENV = os.getenv("APP_ENV", "dev")
ENV_FILE = os.getenv("ENV_FILE")

if ENV_FILE:
    load_dotenv(BASE_DIR / ENV_FILE)
elif (BASE_DIR / ".env").exists():
    load_dotenv(BASE_DIR / ".env")
elif (BASE_DIR / f".env.{APP_ENV}").exists():
    load_dotenv(BASE_DIR / f".env.{APP_ENV}")
elif (BASE_DIR / ".env.dev").exists():
    load_dotenv(BASE_DIR / ".env.dev")


class Settings:
    PROJECT_NAME: str = "Pune Family Concierge"
    APP_ENV: str = os.getenv("APP_ENV", "dev")
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    API_V1_STR: str = "/api/v1"


settings = Settings()
