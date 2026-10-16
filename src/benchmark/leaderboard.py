"""Leaderboard generator for benchmark evaluation results."""
from __future__ import annotations

import csv
import json
import io
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_REPORTS_DIR = Path(r"C:\Projects\CSEB") / "outputs" / "reports"


def generate_leaderboard(
    results_dir: Optional[Path] = None,
    output_csv_path: Optional[Path] = None,
) -> str:
    """Read all benchmark_results_*.json files and generate sorted leaderboard CSV text."""
    if results_dir is None:
        results_dir = DEFAULT_REPORTS_DIR

    results_dir = Path(results_dir)
    json_files = sorted(results_dir.glob("benchmark_results_*.json"))

    rows: List[Dict[str, Any]] = []

    for jf in json_files:
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
            m = data.get("metrics", {})
            rows.append({
                "model_name": data.get("model_name", "unknown"),
                "timestamp": data.get("timestamp", ""),
                "total": data.get("total", 0),
                "passed": data.get("passed", 0),
                "compile_rate": m.get("compile_rate", 0.0),
                "pass_at_1": m.get("pass_at_1", 0.0),
                "avg_complexity_delta": m.get("avg_complexity_delta", 0.0),
            })
        except Exception:
            continue

    # Sort descending by pass_at_1, then compile_rate
    rows.sort(key=lambda r: (r["pass_at_1"], r["compile_rate"]), reverse=True)

    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "model_name",
            "timestamp",
            "total",
            "passed",
            "compile_rate",
            "pass_at_1",
            "avg_complexity_delta",
        ],
        lineterminator="\n",
    )
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

    csv_text = output.getvalue()

    if output_csv_path is None:
        output_csv_path = results_dir / "benchmark_leaderboard.csv"

    Path(output_csv_path).write_text(csv_text, encoding="utf-8")

    return csv_text
