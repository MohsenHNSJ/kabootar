from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


@dataclass
class Settings:
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", "8090"))
    app_secret_key: str = os.getenv("APP_SECRET_KEY", "change-me")

    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")

    channels_address: str = os.getenv("CHANNELS_ADDRESS", "")
    telegram_proxies: str = os.getenv("TELEGRAM_PROXIES", "")

    cron_interval_minutes: int = int(os.getenv("CRON_INTERVAL_MINUTES", "15"))

    rocket_url: str = os.getenv("ROCKET_URL", "")
    rocket_admin_user: str = os.getenv("ROCKET_ADMIN_USER", "")
    rocket_admin_pass: str = os.getenv("ROCKET_ADMIN_PASS", "")
    rocket_room_name: str = os.getenv("ROCKET_ROOM_NAME", "")
    channels_mapping: str = os.getenv("CHANNELS_MAPPING", "")


settings = Settings()


def ensure_data_dir() -> None:
    Path("data").mkdir(parents=True, exist_ok=True)
