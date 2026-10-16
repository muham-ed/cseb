"""Persistence helpers for COBOL programs and their validation results."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.storage.db import get_session, DEFAULT_DB_PATH
from src.storage.models import CobolProgram, BenchmarkTask


def save_program(
    program_id: str,
    generated_cobol: str,
    domain: str,
    source_language: str = "synthetic-template",
    source_license: str = "MIT",
    validation_status: str = "pending",
    loc_count: Optional[int] = None,
    complexity_score: Optional[float] = None,
    db_path: Path = DEFAULT_DB_PATH,
) -> int:
    """Insert or update a CobolProgram row. Returns the row id."""
    session = get_session(db_path)
    try:
        existing = (
            session.query(CobolProgram)
            .filter(CobolProgram.program_id == program_id)
            .one_or_none()
        )
        if loc_count is None:
            loc_count = len(generated_cobol.splitlines())

        if existing:
            existing.generated_cobol = generated_cobol
            existing.domain = domain
            existing.validation_status = validation_status
            existing.loc_count = loc_count
            existing.complexity_score = complexity_score
            row_id = existing.id
        else:
            row = CobolProgram(
                program_id=program_id,
                source_language=source_language,
                source_repo="cseb://templates",
                source_license=source_license,
                generated_cobol=generated_cobol,
                domain=domain,
                loc_count=loc_count,
                complexity_score=complexity_score,
                validation_status=validation_status,
                created_at=datetime.now(timezone.utc).isoformat(),
            )
            session.add(row)
            session.flush()
            row_id = row.id

        session.commit()
        return row_id
    finally:
        session.close()


def count_programs(db_path: Path = DEFAULT_DB_PATH) -> int:
    session = get_session(db_path)
    try:
        return session.query(CobolProgram).count()
    finally:
        session.close()


def count_by_status(db_path: Path = DEFAULT_DB_PATH) -> dict:
    session = get_session(db_path)
    try:
        from sqlalchemy import func
        rows = (
            session.query(CobolProgram.validation_status, func.count())
            .group_by(CobolProgram.validation_status)
            .all()
        )
        return {status: count for status, count in rows}
    finally:
        session.close()


def get_passed_programs(db_path: Path = DEFAULT_DB_PATH) -> List[CobolProgram]:
    """Retrieve all CobolProgram records that have passed validation."""
    session = get_session(db_path)
    try:
        return (
            session.query(CobolProgram)
            .filter(CobolProgram.validation_status == "passed")
            .all()
        )
    finally:
        session.close()


def save_benchmark_task(
    task_id: str,
    instruction_prompt: str,
    complete_prompt: str,
    canonical_solution: str,
    input_files: Optional[Dict[str, Any]] = None,
    output_files: Optional[Dict[str, Any]] = None,
    expected_output: Optional[Any] = None,
    db_path: Path = DEFAULT_DB_PATH,
) -> int:
    """Insert or update a BenchmarkTask row. Returns the row id."""
    session = get_session(db_path)
    try:
        existing = (
            session.query(BenchmarkTask)
            .filter(BenchmarkTask.task_id == task_id)
            .one_or_none()
        )
        if input_files is None:
            input_files = {}
        if output_files is None:
            output_files = {}

        if existing:
            existing.instruction_prompt = instruction_prompt
            existing.complete_prompt = complete_prompt
            existing.canonical_solution = canonical_solution
            existing.input_files = input_files
            existing.output_files = output_files
            existing.expected_output = expected_output
            row_id = existing.id
        else:
            task = BenchmarkTask(
                task_id=task_id,
                instruction_prompt=instruction_prompt,
                complete_prompt=complete_prompt,
                canonical_solution=canonical_solution,
                input_files=input_files,
                output_files=output_files,
                expected_output=expected_output,
            )
            session.add(task)
            session.flush()
            row_id = task.id

        session.commit()
        return row_id
    finally:
        session.close()


def get_all_benchmark_tasks(
    limit: Optional[int] = None,
    db_path: Path = DEFAULT_DB_PATH,
) -> List[BenchmarkTask]:
    """Retrieve all BenchmarkTask records, optionally limited."""
    session = get_session(db_path)
    try:
        query = session.query(BenchmarkTask)
        if limit is not None:
            query = query.limit(limit)
        return query.all()
    finally:
        session.close()


def count_benchmark_tasks(db_path: Path = DEFAULT_DB_PATH) -> int:
    """Return the total number of benchmark tasks in the DB."""
    session = get_session(db_path)
    try:
        return session.query(BenchmarkTask).count()
    finally:
        session.close()
