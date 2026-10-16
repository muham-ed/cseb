"""Evaluator for running language models against CSEB benchmark tasks."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from src.benchmark.metrics import compute_metrics, execution_match

DEFAULT_REPORTS_DIR = Path(r"C:\Projects\CSEB") / "outputs" / "reports"


def evaluate(
    llm_fn: Callable[[str], str],
    tasks: List[Dict[str, Any]],
    out_dir: Optional[Path] = None,
    model_name: str = "llm",
) -> Dict[str, Any]:
    """Run an LLM function against a list of benchmark task dicts.

    tasks: list of dicts with keys:
        - 'task_id': str
        - 'instruction_prompt': str
        - 'complete_prompt': str
        - 'canonical_solution': str
        - 'expected_output': Any
    """
    if out_dir is None:
        out_dir = DEFAULT_REPORTS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    eval_work_dir = out_dir / f"eval_work_{timestamp}"
    eval_work_dir.mkdir(parents=True, exist_ok=True)

    predictions: List[Dict[str, Any]] = []
    references: List[Dict[str, Any]] = []

    for task in tasks:
        task_id = str(task["task_id"])
        prompt = task.get("complete_prompt") or task.get("instruction_prompt", "")
        expected = str(task.get("expected_output", ""))
        canonical = task.get("canonical_solution", "")

        references.append({
            "task_id": task_id,
            "canonical_solution": canonical,
            "expected_output": expected,
        })

        # Generate code with model
        gen_code = llm_fn(prompt)

        # Test generation with execution_match
        safe_name = task_id.replace("-", "_").lower()
        res = execution_match(
            generated_cobol=gen_code,
            expected=expected,
            name=safe_name,
            out_dir=eval_work_dir,
        )

        predictions.append({
            "task_id": task_id,
            "generated_code": gen_code,
            "compiled": res["compiled"],
            "executed": res["executed"],
            "matched": res["matched"],
            "actual": res["actual"],
            "expected": expected,
            "stderr": res["stderr"],
        })

    metrics = compute_metrics(predictions, references)

    report = {
        "model_name": model_name,
        "timestamp": timestamp,
        "total": metrics["total_tasks"],
        "passed": metrics["matched_count"],
        "metrics": metrics,
        "details": predictions,
    }

    report_file = out_dir / f"benchmark_results_{timestamp}.json"
    report_file.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return report
