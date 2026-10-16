"""Rule-based English + Arabic business descriptions for COBOL programs."""
from __future__ import annotations

_TEMPLATE_EN = {
    "ADDITION": "Adds two numeric fields and displays the result under a domain label.",
    "CONDITIONAL": "Compares a value against a threshold and displays one of two messages.",
    "DISPLAY_ONLY": "Displays a predefined message.",
}

_TEMPLATE_AR = {
    "ADDITION": "يجمع حقلين رقميين ويعرض الناتج تحت تسمية المجال.",
    "CONDITIONAL": "يقارن قيمة بحد معين ويعرض إحدى رسالتين حسب النتيجة.",
    "DISPLAY_ONLY": "يعرض رسالة محددة مسبقاً.",
}


def describe(code: str, language: str = "en", template_name: str | None = None) -> str:
    """Return a short natural-language description of the program."""
    table = _TEMPLATE_AR if language == "ar" else _TEMPLATE_EN

    if template_name and template_name in table:
        return table[template_name]

    upper = code.upper()
    if "COMPUTE" in upper or "ADD " in upper:
        return table["ADDITION"]
    if "IF" in upper and "ELSE" in upper:
        return table["CONDITIONAL"]
    if "DISPLAY" in upper:
        return table["DISPLAY_ONLY"]
    return "" if language == "en" else ""