"""Check functional and structural equivalence between original code and generated COBOL."""
from __future__ import annotations

import re


def _normalize_code(code: str) -> list[str]:
    """Strip comments and empty lines, convert to upper case tokens."""
    lines = []
    for line in code.splitlines():
        line_str = line.strip()
        if not line_str or line_str.startswith("*"):
            continue
        lines.append(line_str.upper())
    return lines


def check_equivalence(
    original: str,
    generated: str,
    original_output: str = "",
    generated_output: str = "",
) -> dict:
    """Check structural and execution equivalence between original code and generated code."""
    orig_lines = _normalize_code(original)
    gen_lines = _normalize_code(generated)

    # 1. Output equivalence check
    output_match = False
    if original_output or generated_output:
        output_match = original_output.strip() == generated_output.strip()

    # 2. Key keywords / structure comparison
    orig_keywords = set(re.findall(r"\b[A-Z0-9-]{3,}\b", " ".join(orig_lines)))
    gen_keywords = set(re.findall(r"\b[A-Z0-9-]{3,}\b", " ".join(gen_lines)))

    jaccard_similarity = (
        len(orig_keywords & gen_keywords) / len(orig_keywords | gen_keywords)
        if (orig_keywords | gen_keywords)
        else 1.0
    )

    is_equivalent = output_match or jaccard_similarity > 0.65

    return {
        "equivalent": is_equivalent,
        "output_match": output_match,
        "structural_similarity": round(jaccard_similarity, 4),
        "original_tokens_count": len(orig_keywords),
        "generated_tokens_count": len(gen_keywords),
    }
