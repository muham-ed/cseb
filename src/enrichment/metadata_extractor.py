"""Metadata extraction from COBOL source."""
from __future__ import annotations

import re


def extract_metadata(code: str) -> dict:
    """Extract PROGRAM-ID, LOC, PIC clauses, DIVISION names."""
    meta: dict = {}

    m = re.search(r"PROGRAM-ID\.\s*([A-Z0-9\-]+)", code, re.IGNORECASE)
    meta["program_id"] = m.group(1).upper() if m else None

    meta["loc"] = len(code.splitlines())

    pics = re.findall(r"PIC\s+([A-Z0-9\(\)V\.]+)", code, re.IGNORECASE)
    meta["pic_count"] = len(pics)
    meta["pic_types"] = sorted({p.upper() for p in pics})

    divisions = re.findall(r"(\w+)\s+DIVISION", code, re.IGNORECASE)
    meta["divisions"] = sorted({d.upper() for d in divisions})

    sections = re.findall(r"(\w+)\s+SECTION", code, re.IGNORECASE)
    meta["sections"] = sorted({s.upper() for s in sections})

    return meta