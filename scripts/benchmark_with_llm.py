"""Benchmark evaluation script using real LLM via Ollama."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(r"C:\Projects\CSEB")
sys.path.insert(0, str(ROOT))

from src.storage.db import get_session                                         # noqa: E402
from src.storage.models import BenchmarkTask                                    # noqa: E402
from src.generation.llm_client import OllamaClient, extract_cobol_code          # noqa: E402
from src.benchmark.evaluator import evaluate                                    # noqa: E402
from src.benchmark.leaderboard import generate_leaderboard                       # noqa: E402
from src.common.logging_setup import get_logger                                # noqa: E402

logger = get_logger("benchmark_with_llm")


def main(model_name: str = "qwen2.5-coder:7b") -> int:
    reports_dir = ROOT / "outputs" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    client = OllamaClient(model=model_name)
    if not client.is_available():
        logger.warning(
            f"Ollama server is NOT accessible at {client.host}. "
            f"To run real LLM benchmarks, install Ollama and run `ollama pull {model_name}` followed by `ollama serve`."
        )
        return 1

    session = get_session()
    try:
        db_tasks = session.query(BenchmarkTask).all()
    finally:
        session.close()

    if not db_tasks:
        logger.error("No benchmark tasks found in DB. Run `python scripts/pipeline_v3.py` first.")
        return 1

    logger.info(f"Loaded {len(db_tasks)} benchmark tasks for model '{model_name}'.")

    task_dicts = []
    for t in db_tasks:
        task_dicts.append({
            "task_id": t.task_id,
            "instruction_prompt": t.instruction_prompt,
            "complete_prompt": t.complete_prompt,
            "canonical_solution": t.canonical_solution,
            "expected_output": t.expected_output,
        })

    def llm_fn(prompt: str) -> str:
        raw_out = client.generate(prompt)
        return extract_cobol_code(raw_out)

    report = evaluate(
        llm_fn=llm_fn,
        tasks=task_dicts,
        out_dir=reports_dir,
        model_name=model_name,
    )

    generate_leaderboard(results_dir=reports_dir)

    metrics = report["metrics"]
    logger.info(f"=== Model Evaluation Results ({model_name}) ===")
    logger.info(f"Total Tasks:  {metrics['total_tasks']}")
    logger.info(f"Compile Rate: {metrics['compile_rate'] * 100:.1f}%")
    logger.info(f"Pass Rate:    {metrics['pass_rate'] * 100:.1f}%")

    return 0


if __name__ == "__main__":
    m = sys.argv[1] if len(sys.argv) > 1 else "qwen2.5-coder:7b"
    raise SystemExit(main(model_name=m))
