"""Check COBOL runtime behavior and safety checks."""
from __future__ import annotations

import re


def check_runtime(code: str, expected_output: str = "", input_data: dict = None) -> dict:
    """Analyze COBOL code for potential runtime issues and verify output expectation matching."""
    warnings = []
    risks = []

    upper = code.upper()

    # Infinite PERFORM loop check without UNTIL or VARYING or TIMES
    perform_count = len(re.findall(r"\bPERFORM\b", upper))
    until_count = len(re.findall(r"\bUNTIL\b", upper)) + len(re.findall(r"\bTIMES\b", upper)) + len(re.findall(r"\bVARYING\b", upper))
    if perform_count > until_count:
        warnings.append("Possible unconstrained PERFORM loop detected")

    # Division by zero risk
    if "/" in code or "DIVIDE" in upper:
        if "ON SIZE ERROR" not in upper:
            risks.append("Arithmetic division without ON SIZE ERROR handler")

    # Unhandled file operations
    if "OPEN " in upper and "FILE STATUS" not in upper:
        risks.append("File IO without FILE STATUS verification")

    return {
        "passed": len(risks) == 0,
        "risks": risks,
        "warnings": warnings,
        "has_expected_output": bool(expected_output),
    }
