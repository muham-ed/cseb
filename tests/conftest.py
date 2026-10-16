"""Pytest configuration and shared fixtures for CSEB test suite."""
from __future__ import annotations

import sys
from pathlib import Path
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ROOT = Path(r"C:\Projects\CSEB")
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.storage.models import Base


@pytest.fixture
def tmp_project(tmp_path: Path) -> Path:
    """Fixture providing a temporary project layout."""
    (tmp_path / "data" / "generated" / "cobol").mkdir(parents=True, exist_ok=True)
    (tmp_path / "outputs" / "datasets").mkdir(parents=True, exist_ok=True)
    (tmp_path / "outputs" / "reports").mkdir(parents=True, exist_ok=True)
    return tmp_path


@pytest.fixture
def db_session():
    """Fixture providing an in-memory SQLite SQLAlchemy session."""
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, future=True)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()
