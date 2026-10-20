"""Static COBOL syntax checker."""
from __future__ import annotations

import re


def check_syntax(code: str) -> dict:
    """Perform static syntax analysis on COBOL source code.

    Returns a dict with 'valid': bool, 'errors': list[str], and 'warnings': list[str].
    """
    errors = []
    warnings = []

    if not code or not code.strip():
        return {
            "valid": False,
            "errors": ["Source code is empty"],
            "warnings": [],
        }

    upper = code.upper()

    # 1. Identification Division check
    if "IDENTIFICATION DIVISION" not in upper:
        errors.append("Missing IDENTIFICATION DIVISION")

    # 2. Program ID check
    if "PROGRAM-ID." not in upper:
        errors.append("Missing PROGRAM-ID header")

    # 3. Procedure Division check
    if "PROCEDURE DIVISION" not in upper:
        errors.append("Missing PROCEDURE DIVISION")

    # 4. Stop run or exit check
    if "STOP RUN" not in upper and "GOBACK" not in upper and "EXIT PROGRAM" not in upper:
        warnings.append("No explicit termination statement (STOP RUN / GOBACK) found")

    # 5. Quote balance check
    single_quotes = code.count("'")
    if single_quotes % 2 != 0:
        errors.append("Unmatched single quote in COBOL source")

    double_quotes = code.count('"')
    if double_quotes % 2 != 0:
        errors.append("Unmatched double quote in COBOL source")

    # 6. Basic division ordering check
    id_pos = upper.find("IDENTIFICATION DIVISION")
    proc_pos = upper.find("PROCEDURE DIVISION")
    if id_pos != -1 and proc_pos != -1 and proc_pos < id_pos:
        errors.append("PROCEDURE DIVISION appears before IDENTIFICATION DIVISION")

    is_valid = len(errors) == 0
    return {
        "valid": is_valid,
        "errors": errors,
        "warnings": warnings,
    }
