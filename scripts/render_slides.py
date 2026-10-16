"""Render pitch slides with live database metrics."""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

ROOT = Path(r"C:\Projects\CSEB")
sys.path.insert(0, str(ROOT))

DB_PATH = ROOT / "outputs" / "datasets" / "cseb.db"
SLIDES_TEMPLATE = ROOT / "docs" / "slides" / "cseb_pitch.md"
SLIDES_OUTPUT = ROOT / "docs" / "slides" / "cseb_pitch_rendered.md"


def main() -> int:
    if not DB_PATH.exists():
        print("Database not found. Run pipeline_v3 first.")
        return 1

    conn = sqlite3.connect(DB_PATH)
    try:
        total = conn.execute("SELECT COUNT(*) FROM cobol_programs").fetchone()[0]
        passed = conn.execute("SELECT COUNT(*) FROM cobol_programs WHERE validation_status='passed'").fetchone()[0]
        domains = conn.execute("SELECT COUNT(DISTINCT domain) FROM cobol_programs").fetchone()[0]
        tasks = conn.execute("SELECT COUNT(*) FROM benchmark_tasks").fetchone()[0]
    finally:
        conn.close()

    pass_rate = round((passed / total) * 100, 1) if total > 0 else 0.0

    content = SLIDES_TEMPLATE.read_text(encoding="utf-8")
    rendered = content.format(
        TOTAL_PROGRAMS=total,
        PASS_RATE=pass_rate,
        DOMAINS_COUNT=domains,
        TASKS_COUNT=tasks,
    )

    SLIDES_OUTPUT.write_text(rendered, encoding="utf-8")
    print(f"Rendered slides saved to: {SLIDES_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
