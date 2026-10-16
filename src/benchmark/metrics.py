"""Metrics for benchmark evaluation of COBOL code generation models.

Provides functions to check compilation, execution match against expected output,
and compute aggregate metrics across benchmark tasks.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from src.enrichment.complexity_analyzer import analyze_complexity
from src.validation.gnucobol_runner import (
    compile_cobol,
    run_cobol,
    write_cobol_source,
)

DEFAULT_EVAL_DIR = Path(r"C:\Projects\CSEB") / "data" / "generated" / "cobol" / "eval"


def compile_check(
    generated_cobol: str,
    name: str,
    out_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    """Compile generated COBOL code and return result status and errors."""
    if out_dir is None:
        out_dir = DEFAULT_EVAL_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    cbl_path = out_dir / f"{name}.cbl"
    write_cobol_source(cbl_path, generated_cobol)

    comp_res = compile_cobol(cbl_path)
    return {
        "compiled": comp_res.success,
        "stderr": comp_res.stderr if not comp_res.success else "",
        "exit_code": comp_res.exit_code,
    }


def execution_match(
    generated_cobol: str,
    expected: str,
    name: str,
    out_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    """Compile, run, and compare output of generated COBOL against expected output."""
    if out_dir is None:
        out_dir = DEFAULT_EVAL_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    cbl_path = out_dir / f"{name}.cbl"
    write_cobol_source(cbl_path, generated_cobol)

    comp_res = compile_cobol(cbl_path)
    if not comp_res.success:
        return {
            "compiled": False,
            "executed": False,
            "matched": False,
            "actual": "",
            "expected": expected,
            "stderr": comp_res.stderr,
        }

    run_res = run_cobol(comp_res.exe_path)
    if not run_res.success:
        return {
            "compiled": True,
            "executed": False,
            "matched": False,
            "actual": "",
            "expected": expected,
            "stderr": run_res.stderr,
        }

    actual = run_res.stdout.strip()
    expected_strip = expected.strip() if isinstance(expected, str) else str(expected).strip()
    match = (actual == expected_strip)

    return {
        "compiled": True,
        "executed": True,
        "matched": match,
        "actual": actual,
        "expected": expected_strip,
        "stderr": "",
    }


def compute_metrics(
    predictions: List[Dict[str, Any]],
    references: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Compute aggregate benchmark metrics given predictions and references.

    predictions: list of dicts with keys 'task_id', 'generated_code', 'compiled', 'matched'
    references: list of dicts with keys 'task_id', 'canonical_solution', 'expected_output'
    """
    total = len(references)
    if total == 0:
        return {
            "total_tasks": 0,
            "compiled_count": 0,
            "matched_count": 0,
            "compile_rate": 0.0,
            "match_rate": 0.0,
            "pass_at_1": 0.0,
            "avg_complexity_delta": 0.0,
        }

    ref_map = {r["task_id"]: r for r in references}
    compiled_count = 0
    matched_count = 0
    complexity_deltas: List[float] = []

    for pred in predictions:
        task_id = pred.get("task_id")
        ref = ref_map.get(task_id, {})

        is_compiled = bool(pred.get("compiled", False))
        is_matched = bool(pred.get("matched", False))

        if is_compiled:
            compiled_count += 1
        if is_matched:
            matched_count += 1

        gen_code = pred.get("generated_code", "")
        ref_code = ref.get("canonical_solution", "")
        if gen_code and ref_code:
            gen_comp = analyze_complexity(gen_code)
            ref_comp = analyze_complexity(ref_code)
            complexity_deltas.append(abs(gen_comp - ref_comp))

    compile_rate = compiled_count / total
    match_rate = matched_count / total
    avg_delta = sum(complexity_deltas) / len(complexity_deltas) if complexity_deltas else 0.0

    return {
        "total_tasks": total,
        "compiled_count": compiled_count,
        "matched_count": matched_count,
        "compile_rate": round(compile_rate, 4),
        "match_rate": round(match_rate, 4),
        "pass_at_1": round(match_rate, 4),
        "avg_complexity_delta": round(avg_delta, 4),
    }
