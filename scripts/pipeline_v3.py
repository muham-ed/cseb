"""CSEB v3 pipeline: generate -> validate -> enrich -> store -> build benchmark.

Full pipeline integrating Layer 1 through Layer 5:
  1. Synthetic COBOL generation (templates)
  2. GnuCOBOL validation (compile + run)
  3. Metadata enrichment (complexity, domain, descriptions)
  4. SQLite persistence (CobolProgram)
  5. Benchmark task creation (BenchmarkTask)
  6. Sample task export & leaderboard initialization
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(r"C:\Projects\CSEB")
sys.path.insert(0, str(ROOT))

from src.generation.template_generator import generate                          # noqa: E402
from src.validation.gnucobol_runner import compile_and_run                     # noqa: E402
from src.storage.repository import (                                            # noqa: E402
    save_program,
    count_programs,
    count_by_status,
    get_all_benchmark_tasks,
    count_benchmark_tasks,
)
from src.enrichment.complexity_analyzer import analyze_complexity                 # noqa: E402
from src.enrichment.domain_classifier import classify_domain                      # noqa: E402
from src.enrichment.metadata_extractor import extract_metadata                    # noqa: E402
from src.enrichment.business_describer import describe                            # noqa: E402
from src.benchmark.task_builder import build_tasks                              # noqa: E402
from src.benchmark.leaderboard import generate_leaderboard                      # noqa: E402


def main(count: int = 30, seed: int = 42) -> int:
    out_dir = ROOT / "data" / "generated" / "cobol"
    out_dir.mkdir(parents=True, exist_ok=True)
    reports_dir = ROOT / "outputs" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== CSEB Pipeline v3 (count={count}, seed={seed}) ===\n")

    # --- 1. Generate ---
    print("[1/5] Generating...")
    programs = generate(count=count, seed=seed)
    print(f"      Generated {len(programs)} programs.\n")

    # --- 2. Validate ---
    print("[2/5] Validating (compile + run)...")
    results = []
    for i, prog in enumerate(programs, start=1):
        r = compile_and_run(
            name=f"gen_{prog.program_id}",
            source=prog.source,
            expected=prog.expected_output,
            out_dir=out_dir,
        )
        status = "OK" if r.match else "FAIL"
        print(f"      [{i:03d}/{count}] {prog.program_id} [{status}]")
        results.append((prog, r))

    matched = sum(1 for _, r in results if r.match)
    print(f"\n      Matched: {matched}/{count}\n")

    # --- 3. Enrich ---
    print("[3/5] Enriching...")
    enriched_rows = []
    for prog, r in results:
        meta = extract_metadata(prog.source)
        complexity = analyze_complexity(prog.source)
        domain = classify_domain(prog.source)
        desc_en = describe(prog.source, "en", prog.template_name)
        desc_ar = describe(prog.source, "ar", prog.template_name)
        enriched_rows.append({
            "program_id": prog.program_id,
            "template": prog.template_name,
            "domain": domain,
            "complexity": complexity,
            "loc": meta["loc"],
            "pic_types": meta["pic_types"],
            "description_en": desc_en,
            "description_ar": desc_ar,
            "validation_status": "passed" if r.match else "failed",
            "source": prog.source,
        })
    print(f"      Enriched {len(enriched_rows)} programs.\n")

    # --- 4. Store ---
    print("[4/5] Storing in SQLite...")
    for e in enriched_rows:
        save_program(
            program_id=e["program_id"],
            generated_cobol=e["source"],
            domain=e["domain"],
            validation_status=e["validation_status"],
            complexity_score=e["complexity"],
        )

    total_progs = count_programs()
    by_status = count_by_status()
    print(f"      DB now has {total_progs} programs.")
    print(f"      By status: {by_status}\n")

    # --- 5. Build Benchmark Tasks ---
    print("[5/5] Building Benchmark Tasks...")
    task_ids = build_tasks(out_dir=out_dir)
    total_tasks = count_benchmark_tasks()
    print(f"      Created/Updated {len(task_ids)} benchmark tasks.")
    print(f"      Total benchmark tasks in DB: {total_tasks}\n")

    # Export sample benchmark task
    tasks = get_all_benchmark_tasks(limit=1)
    if tasks:
        sample_task = tasks[0]
        sample_data = {
            "task_id": sample_task.task_id,
            "instruction_prompt": sample_task.instruction_prompt,
            "complete_prompt": sample_task.complete_prompt,
            "canonical_solution": sample_task.canonical_solution,
            "input_files": sample_task.input_files,
            "expected_output": sample_task.expected_output,
        }
        sample_path = reports_dir / "sample_benchmark_task.json"
        sample_path.write_text(
            json.dumps(sample_data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"      Sample benchmark task exported: {sample_path}")

    # Generate initial leaderboard
    leaderboard_csv = generate_leaderboard(results_dir=reports_dir)
    print(f"      Leaderboard updated: {reports_dir / 'benchmark_leaderboard.csv'}")

    print("\n=== Done ===")
    return 0 if matched == count else 1


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    raise SystemExit(main(count=n))
