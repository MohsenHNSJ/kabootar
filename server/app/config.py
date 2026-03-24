from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


@dataclass
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")
    telegram_proxies: str = os.getenv("TELEGRAM_PROXIES", "")


settings = Settings()


def ensure_data_dir() -> None:
    Path("data").mkdir(parents=True, exist_ok=True)
