import json, sqlite3
from pathlib import Path

ROOT = Path(r"C:\Projects\CSEB")
db = ROOT / "outputs" / "datasets" / "cseb.db"
conn = sqlite3.connect(str(db))
c = conn.cursor()

data = {}
data["programs"] = c.execute("SELECT COUNT(*) FROM cobol_programs").fetchone()[0]
data["passed"]   = c.execute("SELECT COUNT(*) FROM cobol_programs WHERE validation_status='passed'").fetchone()[0]
data["tasks"]    = c.execute("SELECT COUNT(*) FROM benchmark_tasks").fetchone()[0]
try:
    data["legal"] = c.execute("SELECT COUNT(*) FROM legal_provenance").fetchone()[0]
except Exception:
    data["legal"] = 0
data["loc"]      = c.execute("SELECT COALESCE(SUM(loc_count),0) FROM cobol_programs").fetchone()[0]
data["domains"]  = [r[0] for r in c.execute("SELECT DISTINCT domain FROM cobol_programs ORDER BY domain").fetchall()]

jsonl = ROOT / "outputs" / "datasets" / "cseb_v1.0.jsonl"
data["jsonl_bytes"] = jsonl.stat().st_size if jsonl.exists() else 0

llm_reports = list((ROOT / "outputs" / "reports").glob("benchmark_llm_*.json"))
data["llm_reports"] = len(llm_reports)

conn.close()
print(json.dumps(data))