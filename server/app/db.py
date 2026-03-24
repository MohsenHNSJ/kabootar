from sqlalchemy import create_engine

from app.config import ensure_data_dir, settings

ensure_data_dir()

engine = create_engine(settings.database_url, future=True)
