"""Template-based COBOL generator (no LLM).

Generates deterministic synthetic COBOL programs by filling in predefined
templates with randomized parameters. Each generated program includes a
known expected output, so validation can compare against it.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Callable, List

from src.generation import templates


@dataclass
class GeneratedProgram:
    program_id: str
    domain: str
    template_name: str
    source: str
    expected_output: str
    parameters: dict = field(default_factory=dict)


_DOMAINS = [
    "accounting", "payroll", "banking", "inventory", "hr", "insurance",
]

_ADD_LABELS = {
    "accounting": "TOTAL: ",
    "payroll": "NET: ",
    "banking": "BALANCE: ",
    "inventory": "STOCK: ",
    "hr": "HOURS: ",
    "insurance": "PREMIUM: ",
}


def _format_cents(cents: int) -> str:
    """Format a cent count the way GnuCOBOL displays PIC 9(6)V99.

    - No decimal point (V is implicit)
    - All digits printed, zero-padded to width 8 (6 integer + 2 decimal)
    """
    return f"{cents:08d}"


def _gen_addition(rng: random.Random, idx: int) -> GeneratedProgram:
    domain = rng.choice(_DOMAINS)
    a = round(rng.uniform(1, 9999), 2)
    b = round(rng.uniform(1, 9999), 2)
    program_id = f"ADD{idx:05d}"
    label = _ADD_LABELS[domain]

    source = templates.ADDITION.format(
        program_id=program_id, a=f"{a:.2f}", b=f"{b:.2f}", label=label
    )

    total_cents = int(round((a + b) * 100))
    expected = f"{label}{_format_cents(total_cents)}"

    return GeneratedProgram(
        program_id=program_id,
        domain=domain,
        template_name="ADDITION",
        source=source,
        expected_output=expected,
        parameters={"a": a, "b": b, "label": label, "total_cents": total_cents},
    )


def _gen_conditional(rng: random.Random, idx: int) -> GeneratedProgram:
    domain = rng.choice(_DOMAINS)
    value = rng.randint(0, 9999)
    threshold = rng.randint(0, 9999)
    program_id = f"COND{idx:05d}"
    high_msg = f"{domain.upper()}-HIGH: value={value} > {threshold}"
    low_msg = f"{domain.upper()}-LOW: value={value} <= {threshold}"

    source = templates.CONDITIONAL.format(
        program_id=program_id,
        value=value,
        threshold=threshold,
        high_msg=high_msg,
        low_msg=low_msg,
    )
    expected = high_msg if value > threshold else low_msg
    return GeneratedProgram(
        program_id=program_id,
        domain=domain,
        template_name="CONDITIONAL",
        source=source,
        expected_output=expected,
        parameters={"value": value, "threshold": threshold},
    )


def _gen_exec_sql(rng: random.Random, idx: int) -> GeneratedProgram:
    domain = rng.choice(_DOMAINS)
    cust_id = rng.randint(10000000, 99999999)
    balance = round(rng.uniform(100, 50000), 2)
    program_id = f"SQL{idx:05d}"
    label = f"{domain.upper()}-SQL-BAL: "

    source = templates.EXEC_SQL.format(
        program_id=program_id,
        cust_id=cust_id,
        balance=f"{balance:.2f}",
        label=label,
    )
    bal_cents = int(round(balance * 100))
    expected = f"{label}{bal_cents:09d}"

    return GeneratedProgram(
        program_id=program_id,
        domain=domain,
        template_name="EXEC_SQL",
        source=source,
        expected_output=expected,
        parameters={"cust_id": cust_id, "balance": balance},
    )


def _gen_exec_cics(rng: random.Random, idx: int) -> GeneratedProgram:
    domain = rng.choice(_DOMAINS)
    trans_id = f"TR{rng.randint(10, 99)}"
    user_id = f"USR{rng.randint(1000, 9999)}"
    program_id = f"CICS{idx:05d}"
    label = f"{domain.upper()}-CICS-TRANS: "

    source = templates.EXEC_CICS.format(
        program_id=program_id,
        trans_id=trans_id,
        user_id=user_id,
        label=label,
    )
    expected = f"{label}{trans_id} U:{user_id}"

    return GeneratedProgram(
        program_id=program_id,
        domain=domain,
        template_name="EXEC_CICS",
        source=source,
        expected_output=expected,
        parameters={"trans_id": trans_id, "user_id": user_id},
    )


_GENERATORS: List[Callable[[random.Random, int], GeneratedProgram]] = [
    _gen_addition,
    _gen_conditional,
    _gen_exec_sql,
    _gen_exec_cics,
]


def generate(count: int, seed: int = 42) -> list:
    """Generate `count` COBOL programs using a deterministic seed."""
    rng = random.Random(seed)
    out = []
    for i in range(count):
        gen = rng.choice(_GENERATORS)
        out.append(gen(rng, i))
    return out