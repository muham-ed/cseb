"""CSEB v1 pipeline: generate -> validate -> store.

Runs the full loop:
  1. Generate N synthetic COBOL programs from templates.
  2. Compile+run each via GnuCOBOL (WSL).
  3. Store results in SQLite.
  4. Print summary.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(r"C:\Projects\CSEB")
sys.path.insert(0, str(ROOT))

from src.generation.template_generator import generate  # noqa: E402
from src.validation.gnucobol_runner import compile_and_run  # noqa: E402
from src.storage.repository import save_program, count_programs, count_by_status  # noqa: E402


def main(count: int = 20, seed: int = 42) -> int:
    out_dir = ROOT / "data" / "generated" / "cobol"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== CSEB Pipeline v1 (count={count}, seed={seed}) ===\n")

    print("[1/3] Generating...")
    programs = generate(count=count, seed=seed)
    print(f"      Generated {len(programs)} programs.\n")

    print("[2/3] Validating (compile + run)...")
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

    compiled = sum(1 for _, r in results if r.compile.success)
    matched = sum(1 for _, r in results if r.match)
    print(f"\n      Compiled: {compiled}/{count}")
    print(f"      Matched:  {matched}/{count}\n")

    print("[3/3] Storing in SQLite...")
    for prog, r in results:
        status = "passed" if r.match else ("failed" if r.compile.success else "compile_error")
        save_program(
            program_id=prog.program_id,
            generated_cobol=prog.source,
            domain=prog.domain,
            validation_status=status,
        )

    total = count_programs()
    by_status = count_by_status()
    print(f"      DB now has {total} programs.")
    print(f"      By status: {by_status}\n")

    print("=== Done ===")
    return 0 if matched == count else 1


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    raise SystemExit(main(count=n))