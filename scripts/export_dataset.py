"""Dataset export CLI script."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(r"C:\Projects\CSEB")
sys.path.insert(0, str(ROOT))

from src.storage.export import export_jsonl, export_parquet, export_sqlite            # noqa: E402
from src.common.logging_setup import get_logger                                        # noqa: E402

logger = get_logger("export_dataset")


def main() -> int:
    datasets_dir = ROOT / "outputs" / "datasets"
    datasets_dir.mkdir(parents=True, exist_ok=True)

    jsonl_path = datasets_dir / "cseb_v1.0.jsonl"
    parquet_path = datasets_dir / "cseb_v1.0.parquet"
    sqlite_path = datasets_dir / "cseb_v1.0.sqlite"

    logger.info("=== CSEB Dataset Export ===")

    n_jsonl = export_jsonl(jsonl_path)
    logger.info(f"JSONL exported:   {jsonl_path} ({n_jsonl} records, {jsonl_path.stat().st_size} bytes)")

    n_parquet = export_parquet(parquet_path)
    logger.info(f"Parquet exported: {parquet_path} ({n_parquet} records, {parquet_path.stat().st_size} bytes)")

    n_sqlite = export_sqlite(sqlite_path)
    logger.info(f"SQLite exported:  {sqlite_path} ({n_sqlite} records, {sqlite_path.stat().st_size} bytes)")

    logger.info("=== Dataset Export Complete ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
