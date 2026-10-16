"""Unit tests for storage repository module."""
from __future__ import annotations

from pathlib import Path
from src.storage.repository import (
    save_program,
    count_programs,
    count_by_status,
    save_benchmark_task,
    count_benchmark_tasks,
    get_all_benchmark_tasks,
)


def test_repository_save_and_update(tmp_path: Path):
    """Test inserting and updating programs and benchmark tasks in SQLite."""
    db_path = tmp_path / "test_cseb.db"

    # 1. Insert program
    row_id = save_program(
        program_id="PROG001",
        generated_cobol="DISPLAY '1'.",
        domain="accounting",
        validation_status="passed",
        db_path=db_path,
    )
    assert row_id > 0
    assert count_programs(db_path) == 1

    # 2. Update program
    save_program(
        program_id="PROG001",
        generated_cobol="DISPLAY '1 UPDATED'.",
        domain="accounting",
        validation_status="passed",
        db_path=db_path,
    )
    assert count_programs(db_path) == 1

    # 3. Status breakdown
    counts = count_by_status(db_path)
    assert counts.get("passed") == 1

    # 4. Save benchmark task
    t_id = save_benchmark_task(
        task_id="CSEB-PROG001",
        instruction_prompt="Write program 1",
        complete_prompt="Task PROG001",
        canonical_solution="DISPLAY '1 UPDATED'.",
        expected_output="1 UPDATED",
        db_path=db_path,
    )
    assert t_id > 0
    assert count_benchmark_tasks(db_path) == 1

    tasks = get_all_benchmark_tasks(db_path=db_path)
    assert len(tasks) == 1
    assert tasks[0].task_id == "CSEB-PROG001"
