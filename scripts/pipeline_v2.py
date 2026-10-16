"""CSEB v2 pipeline: generate -> validate -> enrich -> store.

Adds Layer 3 (Enrichment) on top of v1:
  - Cyclomatic complexity
  - Domain classification
  - Metadata extraction
  - English + Arabic descriptions
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(r"C:\Projects\CSEB")
sys.path.insert(0, str(ROOT))

from src.generation.template_generator import generate          # noqa: E402
from src.validation.gnucobol_runner import compile_and_run     # noqa: E402
from src.storage.repository import save_program, count_programs, count_by_status  # noqa: E402
from src.enrichment.complexity_analyzer import analyze_complexity  # noqa: E402
from src.enrichment.domain_classifier import classify_domain       # noqa: E402
from src.enrichment.metadata_extractor import extract_metadata     # noqa: E402
from src.enrichment.business_describer import describe             # noqa: E402


def main(count: int = 20, seed: int = 42) -> int:
    out_dir = ROOT / "data" / "generated" / "cobol"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== CSEB Pipeline v2 (count={count}, seed={seed}) ===\n")

    # --- 1. Generate ---
    print("[1/4] Generating...")
    programs = generate(count=count, seed=seed)
    print(f"      Generated {len(programs)} programs.\n")

    # --- 2. Validate ---
    print("[2/4] Validating (compile + run)...")
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
    print("[3/4] Enriching...")
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
    print("[4/4] Storing in SQLite...")
    for e in enriched_rows:
        save_program(
            program_id=e["program_id"],
            generated_cobol=e["source"],
            domain=e["domain"],
            validation_status=e["validation_status"],
            complexity_score=e["complexity"],
        )

    total = count_programs()
    by_status = count_by_status()
    print(f"      DB now has {total} programs.")
    print(f"      By status: {by_status}\n")

    # Save enriched JSON (without raw source to keep it readable)
    report_path = ROOT / "outputs" / "reports" / "enriched_v2.json"
    clean = [{k: v for k, v in e.items() if k != "source"} for e in enriched_rows]
    report_path.write_text(
        json.dumps(clean, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"      Enriched report: {report_path}")

    # Print a sample
    print("\n=== Sample enriched program ===")
    sample = clean[0]
    for k in ("program_id", "template", "domain", "complexity", "loc",
              "description_en", "description_ar"):
        print(f"  {k}: {sample[k]}")

    print("\n=== Done ===")
    return 0 if matched == count else 1


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    raise SystemExit(main(count=n))