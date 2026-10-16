"""Cyclomatic complexity analyzer for COBOL programs.

Counts decision points (IF, WHEN, UNTIL, AND, OR) in executable code,
ignoring comment lines (column 7 = '*') and scope terminators (e.g. END-IF).
"""
from __future__ import annotations

import re

_DECISION_TOKENS = [
    r"(?<!END-)\bIF\b",
    r"(?<!END-)\bWHEN\b",
    r"\bUNTIL\b",
    r"\bAND\b",
    r"\bOR\b",
]


def _strip_comments(code: str) -> str:
    """Remove COBOL comment lines (column 7 is '*')."""
    lines = []
    for line in code.splitlines():
        if len(line) >= 7 and line[6] == "*":
            continue
        lines.append(line)
    return "\n".join(lines)


def analyze_complexity(code: str) -> float:
    """Return McCabe cyclomatic complexity: 1 + number of decision points."""
    clean = _strip_comments(code)
    count = 0
    for token in _DECISION_TOKENS:
        count += len(re.findall(token, clean, flags=re.IGNORECASE))
    return float(1 + count)
