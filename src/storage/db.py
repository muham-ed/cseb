"""SQLite database initialization."""
from __future__ import annotations

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.storage.models import Base

DEFAULT_DB_PATH = Path(r"C:\Projects\CSEB\outputs\datasets\cseb.db")


def get_engine(db_path: Path = DEFAULT_DB_PATH):
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(f"sqlite:///{db_path.as_posix()}", future=True)


def get_session(db_path: Path = DEFAULT_DB_PATH):
    engine = get_engine(db_path)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, future=True)()


def init_db(db_path: Path = DEFAULT_DB_PATH) -> Path:
    """Create all tables and return the DB path."""
    engine = get_engine(db_path)
    Base.metadata.create_all(engine)
    engine.dispose()
    return db_path