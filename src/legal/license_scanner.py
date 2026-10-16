"""License scanner for identifying SPDX license headers in source code."""
from __future__ import annotations

import re
from pathlib import Path


def scan_license(file_path: str | Path) -> str:
    """Scan a file for SPDX-License-Identifier or common open source license notices."""
    path = Path(file_path)
    if not path.exists():
        return "unknown"

    content = path.read_text(encoding="utf-8", errors="ignore")

    # Match SPDX-License-Identifier: <LICENSE>
    spdx_match = re.search(r"SPDX-License-Identifier:\s*([A-Za-z0-9\.\-\+]+)", content)
    if spdx_match:
        return spdx_match.group(1)

    upper = content.upper()
    if "MIT LICENSE" in upper or "PERMISSION IS HEREBY GRANTED" in upper:
        return "MIT"
    if "APACHE LICENSE" in upper or "APACHE-2.0" in upper:
        return "Apache-2.0"
    if "GNU GENERAL PUBLIC LICENSE" in upper or "GPL" in upper:
        return "GPL-3.0-or-later"
    if "BSD" in upper:
        return "BSD-3-Clause"

    return "MIT"  # Default assumption for repository template sources
