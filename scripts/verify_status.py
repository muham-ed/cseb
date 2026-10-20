import sqlite3, sys
from pathlib import Path

ROOT = Path(r"C:\Projects\CSEB")
db = ROOT / "outputs" / "datasets" / "cseb.db"

print(f"docs/STATUS.md exists: {(ROOT / 'docs' / 'STATUS.md').exists()}")

if not db.exists():
    print(f"DB missing: {db}")
    sys.exit(1)

conn = sqlite3.connect(str(db))
c = conn.cursor()

programs = c.execute("SELECT COUNT(*) FROM cobol_programs").fetchone()[0]
passed = c.execute("SELECT COUNT(*) FROM cobol_programs WHERE validation_status='passed'").fetchone()[0]
tasks = c.execute("SELECT COUNT(*) FROM benchmark_tasks").fetchone()[0]
try:
    legal = c.execute("SELECT COUNT(*) FROM legal_provenance").fetchone()[0]
except Exception:
    legal = "table missing"

print(f"cobol_programs:    {programs}")
print(f"passed:            {passed}")
print(f"benchmark_tasks:   {tasks}")
print(f"legal_provenance:  {legal}")

# Total LOC
loc = c.execute("SELECT COALESCE(SUM(loc_count),0) FROM cobol_programs").fetchone()[0]
print(f"total LOC:         {loc}")

# Total dataset size
jsonl = ROOT / "outputs" / "datasets" / "cseb_v1.0.jsonl"
if jsonl.exists():
    print(f"JSONL size:        {jsonl.stat().st_size:,} bytes")

conn.close()

# Coverage check
import re
cov_file = ROOT / ".coverage"
print(f".coverage exists:  {cov_file.exists()}")