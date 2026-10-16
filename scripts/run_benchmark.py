"""Benchmark runner test script using a dummy echo LLM.

Validates the evaluation harness end-to-end by passing canonical solutions
back as model generations. Asserts 100% pass rate.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(r"C:\Projects\CSEB")
sys.path.insert(0, str(ROOT))

from src.storage.repository import get_all_benchmark_tasks                     # noqa: E402
from src.benchmark.evaluator import evaluate                                   # noqa: E402
from src.benchmark.leaderboard import generate_leaderboard                      # noqa: E402


def main() -> int:
    reports_dir = ROOT / "outputs" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    print("=== CSEB Benchmark Evaluation Harness Test ===")

    # 1. Fetch benchmark tasks from DB
    db_tasks = get_all_benchmark_tasks()
    if not db_tasks:
        print("ERROR: No benchmark tasks found in DB. Run pipeline_v3.py first!")
        return 1

    print(f"Loaded {len(db_tasks)} benchmark tasks from database.")

    # 2. Build task dictionaries and lookup map for dummy LLM
    task_dicts = []
    prompt_to_solution = {}

    for t in db_tasks:
        prompt = t.complete_prompt or t.instruction_prompt or ""
        solution = t.canonical_solution or ""
        td = {
            "task_id": t.task_id,
            "instruction_prompt": t.instruction_prompt,
            "complete_prompt": prompt,
            "canonical_solution": solution,
            "expected_output": t.expected_output,
        }
        task_dicts.append(td)
        prompt_to_solution[prompt] = solution

    # 3. Dummy Echo LLM: returns canonical solution for given prompt
    def dummy_echo_llm(prompt: str) -> str:
        return prompt_to_solution.get(prompt, "")

    # 4. Evaluate dummy LLM
    print("\nRunning evaluation with Dummy Echo LLM...")
    res = evaluate(
        llm_fn=dummy_echo_llm,
        tasks=task_dicts,
        out_dir=reports_dir,
        model_name="dummy_echo_v1",
    )

    # 5. Generate updated leaderboard
    leaderboard_csv = generate_leaderboard(results_dir=reports_dir)

    metrics = res["metrics"]
    total = metrics["total_tasks"]
    matched = metrics["matched_count"]
    pass_rate = metrics["pass_at_1"]

    print("\n=== Evaluation Summary ===")
    print(f"  Model:        {res['model_name']}")
    print(f"  Total Tasks:  {total}")
    print(f"  Passed Tasks: {matched}")
    print(f"  Compile Rate: {metrics['compile_rate'] * 100:.1f}%")
    print(f"  Pass Rate:    {pass_rate * 100:.1f}%")

    print("\n=== Leaderboard CSV ===")
    print(leaderboard_csv.strip())

    if pass_rate == 1.0 and matched == total:
        print("\nSUCCESS: Evaluation harness validated! 100% pass rate achieved.")
        return 0
    else:
        print(f"\nFAILURE: Harness produced unexpected pass rate {pass_rate} ({matched}/{total})")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
