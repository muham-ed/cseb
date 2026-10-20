"""Unit tests for newly implemented CSEB components."""
from __future__ import annotations

from pathlib import Path
from src.generation.template_generator import generate
from src.validation.syntax_checker import check_syntax
from src.validation.runtime_checker import check_runtime
from src.validation.equivalence_checker import check_equivalence
from src.validation.validation_report import generate_report
from src.enrichment.dependency_mapper import map_dependencies
from src.legal.provenance_tracker import track_provenance
from src.legal.compliance_checker import check_compliance
from src.legal.legal_report import generate_legal_report
from src.storage.export import export_huggingface, export_sqlite, export_jsonl, export_parquet
from src.storage.db import init_db
from src.storage.repository import save_program


def test_syntax_checker_valid_and_invalid():
    valid_cobol = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. TEST01.
       PROCEDURE DIVISION.
           DISPLAY 'HELLO WORLD'.
           STOP RUN.
    """
    res_valid = check_syntax(valid_cobol)
    assert res_valid["valid"] is True
    assert len(res_valid["errors"]) == 0

    invalid_cobol = "PROCEDURE DIVISION. DISPLAY 'HELLO."
    res_invalid = check_syntax(invalid_cobol)
    assert res_invalid["valid"] is False
    assert len(res_invalid["errors"]) > 0


def test_runtime_checker():
    cobol = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. TEST02.
       PROCEDURE DIVISION.
           PERFORM VARYING I FROM 1 BY 1 UNTIL I > 10
               DISPLAY I
           END-PERFORM.
           STOP RUN.
    """
    res = check_runtime(cobol, expected_output="10")
    assert res["passed"] is True
    assert res["has_expected_output"] is True


def test_equivalence_checker():
    code1 = "IDENTIFICATION DIVISION. PROGRAM-ID. P1. PROCEDURE DIVISION. DISPLAY 'A'. STOP RUN."
    code2 = "IDENTIFICATION DIVISION. PROGRAM-ID. P1. PROCEDURE DIVISION. DISPLAY 'A'. STOP RUN."

    res = check_equivalence(code1, code2, original_output="A", generated_output="A")
    assert res["equivalent"] is True
    assert res["output_match"] is True


def test_validation_report():
    report_json = generate_report([], format_type="json")
    assert "total_programs" in report_json

    report_html = generate_report([], format_type="html")
    assert "<html>" in report_html.lower()


def test_dependency_mapper():
    code = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. TEST03.
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT MY-FILE ASSIGN TO CUSTFILE.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
           COPY CUSTREC.
       PROCEDURE DIVISION.
           EXEC SQL SELECT * FROM USERS END-EXEC.
           EXEC CICS SEND TEXT FROM('HI') END-EXEC.
           CALL 'SUBPROG'.
           STOP RUN.
    """
    deps = map_dependencies(code)
    assert "CUSTREC" in deps["copybooks"]
    assert "SUBPROG" in deps["calls"]
    assert deps["db2_sql"] is True
    assert deps["cics_trans"] is True
    assert "EXEC_SQL" in deps["features"]


def test_provenance_tracker():
    rec = track_provenance(program_id="PROG100", source_code="DISPLAY 'TEST'.")
    assert rec["program_id"] == "PROG100"
    assert len(rec["sha256_hash"]) == 64
    assert "SPDX-License-Identifier" in rec["spdx_identifier"]


def test_compliance_and_legal_report(tmp_path: Path):
    db_path = tmp_path / "test_cseb.db"
    init_db(db_path)
    save_program(
        program_id="COMP001",
        generated_cobol="DISPLAY 'COMPLIANCE'.",
        domain="banking",
        source_license="MIT",
        db_path=db_path,
    )

    comp = check_compliance("COMP001", db_path=db_path)
    assert comp["compliant"] is True
    assert comp["license"] == "MIT"

    report_text = generate_legal_report(db_path=db_path, out_format="text")
    assert "FULLY COMPLIANT" in report_text


def test_export_huggingface(tmp_path: Path):
    db_path = tmp_path / "test_cseb.db"
    init_db(db_path)
    save_program(
        program_id="HF001",
        generated_cobol="DISPLAY 'HF'.",
        domain="accounting",
        validation_status="passed",
        db_path=db_path,
    )

    out_dir = tmp_path / "hf_dataset"
    count = export_huggingface(out_dir, db_path=db_path)
    assert count == 1
    assert (out_dir / "dataset_info.json").exists()
    assert (out_dir / "README.md").exists()
    assert (out_dir / "data" / "train-00000-of-00001.parquet").exists()


def test_enterprise_templates_generation():
    progs = generate(count=20, seed=123)
    assert len(progs) == 20
    template_names = {p.template_name for p in progs}
    assert "EXEC_SQL" in template_names or "EXEC_CICS" in template_names or "ADDITION" in template_names
