"""Build benchmark tasks from validated COBOL programs in the database.

Reads all 'passed' programs from the SQLite database, extracts prompts and
metadata, computes expected output if needed, and saves/updates BenchmarkTask records.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from src.storage.db import DEFAULT_DB_PATH
from src.storage.repository import (
    get_passed_programs,
    save_benchmark_task,
)
from src.validation.gnucobol_runner import compile_and_run


def generate_prompts(program_id: str, code: str, domain: str) -> tuple[str, str]:
    """Generate instruction_prompt and complete_prompt based on program code and domain."""
    upper = code.upper()
    if "COMPUTE" in upper or "ADD " in upper:
        instruction = (
            f"Write a COBOL-85 program for the {domain} domain that performs arithmetic addition "
            f"on numeric fields (PIC 9(5)V99) and displays the total under a label."
        )
    elif "IF" in upper and "ELSE" in upper:
        instruction = (
            f"Write a COBOL-85 program for the {domain} domain that compares a numeric value "
            f"against a threshold and displays a high or low status message."
        )
    else:
        instruction = (
            f"Write a COBOL-85 program for the {domain} domain that produces the expected "
            f"output line."
        )

    complete_prompt = (
        f"Task ID: CSEB-{program_id}\n"
        f"Domain: {domain}\n"
        f"Instruction: {instruction}\n\n"
        f"Write a complete, compilable COBOL-85 program in fixed format starting at column 8."
    )

    return instruction, complete_prompt


def build_tasks(
    limit: Optional[int] = None,
    db_path: Path = DEFAULT_DB_PATH,
    out_dir: Optional[Path] = None,
) -> List[str]:
    """Build benchmark tasks from all passed COBOL programs in DB.

    Returns list of created task_ids (e.g. ['CSEB-ADD00000', ...]).
    """
    if out_dir is None:
        out_dir = Path(r"C:\Projects\CSEB") / "data" / "generated" / "cobol"

    passed_programs = get_passed_programs(db_path)
    if limit is not None:
        passed_programs = passed_programs[:limit]

    created_task_ids: List[str] = []

    for prog in passed_programs:
        task_id = f"CSEB-{prog.program_id}"
        code = prog.generated_cobol or ""
        domain = prog.domain or "general"

        instruction_prompt, complete_prompt = generate_prompts(
            prog.program_id, code, domain
        )

        # Run compile_and_run to guarantee we get the exact expected output line
        res = compile_and_run(
            name=f"task_{prog.program_id}",
            source=code,
            expected="",
            out_dir=out_dir,
        )
        expected_stdout = res.output_line if res.compile.success else ""

        input_files = {
            "domain": domain,
            "program_id": prog.program_id,
            "loc_count": prog.loc_count,
            "complexity_score": prog.complexity_score,
        }
        output_files = {}

        save_benchmark_task(
            task_id=task_id,
            instruction_prompt=instruction_prompt,
            complete_prompt=complete_prompt,
            canonical_solution=code,
            input_files=input_files,
            output_files=output_files,
            expected_output=expected_stdout,
            db_path=db_path,
        )

        created_task_ids.append(task_id)

    return created_task_ids
