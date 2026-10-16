"""Runner for compiling and validating real open-source COBOL files."""
from __future__ import annotations

import json
from pathlib import Path
from src.validation.gnucobol_runner import compile_and_run
from src.common.logging_setup import get_logger

logger = get_logger("real_source_runner")


def run_real_sources(
    manifest_path: Path,
    out_dir: Path,
) -> dict:
    """Compile and execute all real COBOL sources listed in manifest."""
    manifest_path = Path(manifest_path)
    if not manifest_path.exists():
        logger.error(f"Manifest not found: {manifest_path}")
        return {"total": 0, "compiled": 0}

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    total = len(manifest)
    compiled = 0

    results = []
    for item in manifest:
        rel_file = item["file"]
        file_path = manifest_path.parent.parent.parent / rel_file
        if not file_path.exists():
            continue

        source = file_path.read_text(encoding="utf-8")
        name = file_path.stem

        res = compile_and_run(
            name=f"real_{name}",
            source=source,
            expected="",
            out_dir=out_dir,
        )

        if res.compile.success:
            compiled += 1

        results.append({
            "name": name,
            "compiled": res.compile.success,
            "stdout": res.output_line,
        })

    logger.info(f"Real COBOL sources result: {compiled}/{total} compiled successfully.")
    return {"total": total, "compiled": compiled, "details": results}
