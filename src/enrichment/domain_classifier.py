"""Keyword-based business domain classifier for COBOL programs."""
from __future__ import annotations

_DOMAIN_KEYWORDS = {
    "accounting": ["TOTAL:", "INVOICE", "ACCT", "AMOUNT", "LEDGER"],
    "payroll":    ["NET:", "PAYROLL", "GROSS", "SALARY", "WAGE"],
    "banking":    ["BALANCE:", "BANK", "ACCOUNT", "DEPOSIT", "WITHDRAW"],
    "inventory":  ["STOCK:", "REORDER", "QTY", "WAREHOUSE", "ITEM"],
    "hr":         ["HOURS:", "EMPLOYEE", "STAFF", "HR-", "ATTEND"],
    "insurance":  ["PREMIUM:", "POLICY", "INS-", "CLAIM", "COVERAGE"],
}


def classify_domain(code: str) -> str:
    """Return the best-matching domain, or 'unknown' if no keyword matches."""
    upper = code.upper()
    scores = {d: 0 for d in _DOMAIN_KEYWORDS}
    for domain, kws in _DOMAIN_KEYWORDS.items():
        for kw in kws:
            if kw.upper() in upper:
                scores[domain] += 1
    best_domain, best_score = max(scores.items(), key=lambda kv: kv[1])
    return best_domain if best_score > 0 else "unknown"


def all_domain_scores(code: str) -> dict:
    upper = code.upper()
    return {
        d: sum(1 for kw in kws if kw.upper() in upper)
        for d, kws in _DOMAIN_KEYWORDS.items()
    }