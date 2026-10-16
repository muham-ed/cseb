"""Export dataset to JSONL, Parquet, and SQLite formats."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
import pandas as pd

from src.storage.db import DEFAULT_DB_PATH, get_session
from src.storage.models import CobolProgram


def export_jsonl(out_path: Path, db_path: Path = DEFAULT_DB_PATH) -> int:
    """Export all passed COBOL programs to JSONL format. Returns record count."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    session = get_session(db_path)
    try:
        rows = (
            session.query(CobolProgram)
            .filter(CobolProgram.validation_status == "passed")
            .all()
        )
        records = []
        for r in rows:
            records.append({
                "program_id": r.program_id,
                "domain": r.domain,
                "loc_count": r.loc_count,
                "complexity_score": r.complexity_score,
                "source_language": r.source_language,
                "source_license": r.source_license,
                "generated_cobol": r.generated_cobol,
                "validation_status": r.validation_status,
                "created_at": r.created_at,
            })

        lines = [json.dumps(rec, ensure_ascii=False) for rec in records]
        out_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
        return len(records)
    finally:
        session.close()


def export_parquet(out_path: Path, db_path: Path = DEFAULT_DB_PATH) -> int:
    """Export all passed COBOL programs to Parquet format. Returns record count."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(
            "SELECT * FROM cobol_programs WHERE validation_status = 'passed'", conn
        )
        df.to_parquet(out_path, index=False)
        return len(df)
    finally:
        conn.close()


def export_sqlite(out_path: Path, db_path: Path = DEFAULT_DB_PATH) -> int:
    """Export standalone SQLite dataset file using VACUUM INTO. Returns record count."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        out_path.unlink()

    conn = sqlite3.connect(db_path)
    try:
        conn.execute(f"VACUUM INTO '{out_path.as_posix()}'")
        count = conn.execute(
            "SELECT COUNT(*) FROM cobol_programs WHERE validation_status = 'passed'"
        ).fetchone()[0]
        return count
    finally:
        conn.close()
