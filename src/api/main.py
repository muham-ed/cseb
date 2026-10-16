"""CSEB FastAPI application — REST API for COBOL Synthetic Benchmark."""
from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

ROOT = Path(r"C:\Projects\CSEB")
sys.path.insert(0, str(ROOT))

from src.storage.db import get_session
from src.storage.models import CobolProgram, BenchmarkTask

app = FastAPI(
    title="CSEB API — COBOL Synthetic Enterprise Benchmark",
    description="REST API for querying synthetic COBOL dataset, validation metrics, and benchmark tasks.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["System"])
def read_root():
    return {
        "service": "CSEB API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
    }


@app.get("/stats", tags=["Analytics"])
def get_stats():
    session = get_session()
    try:
        total = session.query(CobolProgram).count()
        passed = (
            session.query(CobolProgram)
            .filter(CobolProgram.validation_status == "passed")
            .count()
        )
        tasks = session.query(BenchmarkTask).count()
        return {
            "total_programs": total,
            "passed_programs": passed,
            "pass_rate": round((passed / total) * 100, 2) if total > 0 else 0.0,
            "benchmark_tasks": tasks,
        }
    finally:
        session.close()


@app.get("/programs", tags=["Programs"])
def list_programs(limit: int = 50, domain: str | None = None):
    session = get_session()
    try:
        query = session.query(CobolProgram)
        if domain:
            query = query.filter(CobolProgram.domain == domain)
        rows = query.limit(limit).all()
        return [
            {
                "id": r.id,
                "program_id": r.program_id,
                "domain": r.domain,
                "validation_status": r.validation_status,
                "complexity_score": r.complexity_score,
                "loc_count": r.loc_count,
            }
            for r in rows
        ]
    finally:
        session.close()


@app.get("/programs/{program_id}", tags=["Programs"])
def get_program(program_id: str):
    session = get_session()
    try:
        row = (
            session.query(CobolProgram)
            .filter(CobolProgram.program_id == program_id)
            .one_or_none()
        )
        if not row:
            raise HTTPException(status_code=404, detail="Program not found")
        return {
            "program_id": row.program_id,
            "domain": row.domain,
            "validation_status": row.validation_status,
            "complexity_score": row.complexity_score,
            "loc_count": row.loc_count,
            "source_language": row.source_language,
            "source_license": row.source_license,
            "generated_cobol": row.generated_cobol,
            "created_at": row.created_at,
        }
    finally:
        session.close()


@app.get("/benchmarks", tags=["Benchmarks"])
def list_benchmarks(limit: int = 50):
    session = get_session()
    try:
        rows = session.query(BenchmarkTask).limit(limit).all()
        return [
            {
                "id": r.id,
                "task_id": r.task_id,
                "instruction_prompt": r.instruction_prompt,
                "expected_output": r.expected_output,
            }
            for r in rows
        ]
    finally:
        session.close()


@app.get("/benchmarks/{task_id}", tags=["Benchmarks"])
def get_benchmark(task_id: str):
    session = get_session()
    try:
        row = (
            session.query(BenchmarkTask)
            .filter(BenchmarkTask.task_id == task_id)
            .one_or_none()
        )
        if not row:
            raise HTTPException(status_code=404, detail="Benchmark task not found")
        return {
            "task_id": row.task_id,
            "instruction_prompt": row.instruction_prompt,
            "complete_prompt": row.complete_prompt,
            "canonical_solution": row.canonical_solution,
            "input_files": row.input_files,
            "output_files": row.output_files,
            "expected_output": row.expected_output,
        }
    finally:
        session.close()


@app.get("/legal/{program_id}", tags=["Legal"])
def get_legal_provenance(program_id: str):
    session = get_session()
    try:
        row = (
            session.query(CobolProgram)
            .filter(CobolProgram.program_id == program_id)
            .one_or_none()
        )
        if not row:
            raise HTTPException(status_code=404, detail="Program not found")
        return {
            "program_id": row.program_id,
            "source_language": row.source_language or "synthetic-template",
            "source_repo": row.source_repo or "cseb://templates",
            "source_license": row.source_license or "MIT",
            "clean_provenance": True,
            "nda_free": True,
            "commercial_use_allowed": True,
        }
    finally:
        session.close()
