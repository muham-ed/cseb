"""Generate validation reports in JSON or HTML format."""
from __future__ import annotations

import json


def generate_report(results: list, format_type: str = "json") -> str:
    """Generate summary validation report across test results."""
    total = len(results)
    passed = sum(1 for r in results if getattr(r, "match", False) or (isinstance(r, dict) and r.get("match")))
    failed = total - passed
    pass_rate = (passed / total * 100.0) if total > 0 else 0.0

    summary = {
        "total_programs": total,
        "passed": passed,
        "failed": failed,
        "pass_rate_pct": round(pass_rate, 2),
    }

    if format_type.lower() == "html":
        return f"""<!DOCTYPE html>
<html>
<head><title>CSEB Validation Report</title></head>
<body>
<h1>CSEB Validation Report</h1>
<p>Total Programs: <strong>{total}</strong></p>
<p>Passed: <strong style="color:green;">{passed}</strong></p>
<p>Failed: <strong style="color:red;">{failed}</strong></p>
<p>Pass Rate: <strong>{pass_rate:.2f}%</strong></p>
</body>
</html>"""

    return json.dumps(summary, indent=2)
