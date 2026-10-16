"""Unit tests for benchmark metrics, evaluator, and leaderboard modules."""
from __future__ import annotations

from pathlib import Path
from src.benchmark.metrics import compile_check, execution_match, compute_metrics
from src.benchmark.evaluator import evaluate
from src.benchmark.leaderboard import generate_leaderboard


def test_compile_check_valid_and_invalid(tmp_path: Path):
    """Test compile_check with valid and invalid COBOL."""
    valid_cobol = """\
       IDENTIFICATION DIVISION.
       PROGRAM-ID. CHK1.
       PROCEDURE DIVISION.
           DISPLAY 'OK'.
           STOP RUN.
"""
    res1 = compile_check(valid_cobol, "chk1", out_dir=tmp_path)
    assert res1["compiled"] is True

    invalid_cobol = "INVALID COBOL CODE"
    res2 = compile_check(invalid_cobol, "chk2", out_dir=tmp_path)
    assert res2["compiled"] is False


def test_execution_match(tmp_path: Path):
    """Test execution_match for matching and non-matching outputs."""
    cobol = """\
       IDENTIFICATION DIVISION.
       PROGRAM-ID. CHK3.
       PROCEDURE DIVISION.
           DISPLAY 'MATCH_TEST'.
           STOP RUN.
"""
    res1 = execution_match(cobol, "MATCH_TEST", "chk3", out_dir=tmp_path)
    assert res1["compiled"] is True
    assert res1["executed"] is True
    assert res1["matched"] is True

    res2 = execution_match(cobol, "WRONG_TEST", "chk3_b", out_dir=tmp_path)
    assert res2["matched"] is False


def test_compute_metrics():
    """Test compute_metrics aggregation."""
    preds = [
        {"task_id": "T1", "compiled": True, "matched": True, "generated_code": "DISPLAY 'A'."},
        {"task_id": "T2", "compiled": True, "matched": False, "generated_code": "DISPLAY 'B'."},
    ]
    refs = [
        {"task_id": "T1", "canonical_solution": "DISPLAY 'A'.", "expected_output": "A"},
        {"task_id": "T2", "canonical_solution": "DISPLAY 'B'.", "expected_output": "B"},
    ]
    metrics = compute_metrics(preds, refs)
    assert metrics["total_tasks"] == 2
    assert metrics["compiled_count"] == 2
    assert metrics["matched_count"] == 1
    assert metrics["compile_rate"] == 1.0
    assert metrics["match_rate"] == 0.5


def test_evaluator_and_leaderboard(tmp_path: Path):
    """Test evaluate function and leaderboard generation."""
    tasks = [
        {
            "task_id": "CSEB-T1",
            "instruction_prompt": "Write program T1",
            "complete_prompt": "Task T1",
            "canonical_solution": """\
       IDENTIFICATION DIVISION.
       PROGRAM-ID. T1.
       PROCEDURE DIVISION.
           DISPLAY 'HELLO T1'.
           STOP RUN.
""",
            "expected_output": "HELLO T1",
        }
    ]

    def dummy_llm(prompt: str) -> str:
        return tasks[0]["canonical_solution"]

    eval_res = evaluate(dummy_llm, tasks, out_dir=tmp_path, model_name="dummy_test")
    assert eval_res["total"] == 1
    assert eval_res["passed"] == 1

    csv_text = generate_leaderboard(results_dir=tmp_path)
    assert "dummy_test" in csv_text
    assert "1.0" in csv_text
