"""Map dependencies and enterprise features (Copybooks, Subprograms, DB2, CICS, VSAM) in COBOL source code."""
from __future__ import annotations

import re


def map_dependencies(code: str) -> dict:
    """Analyze COBOL source code and return a dictionary of identified enterprise dependencies."""
    if not code:
        return {
            "copybooks": [],
            "calls": [],
            "db2_sql": False,
            "cics_trans": False,
            "vsam_files": [],
            "features": [],
        }

    copybooks = re.findall(r"\bCOPY\s+([A-Za-z0-9_-]+)", code, re.IGNORECASE)
    calls = re.findall(r"\bCALL\s+['\"]([A-Za-z0-9_-]+)['\"]", code, re.IGNORECASE)
    db2_sql = bool(re.search(r"\bEXEC\s+SQL\b", code, re.IGNORECASE))
    cics_trans = bool(re.search(r"\bEXEC\s+CICS\b", code, re.IGNORECASE))
    vsam_files = re.findall(r"\bASSIGN\s+TO\s+([A-Za-z0-9_-]+)", code, re.IGNORECASE)

    features = []
    if copybooks:
        features.append("COPYBOOK")
    if calls:
        features.append("SUBPROGRAM_CALL")
    if db2_sql:
        features.append("EXEC_SQL")
    if cics_trans:
        features.append("EXEC_CICS")
    if vsam_files:
        features.append("VSAM_FILE")

    return {
        "copybooks": list(set(copybooks)),
        "calls": list(set(calls)),
        "db2_sql": db2_sql,
        "cics_trans": cics_trans,
        "vsam_files": list(set(vsam_files)),
        "features": features,
    }
