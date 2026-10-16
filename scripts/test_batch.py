"""Batch smoke test using the real gnucobol_runner module."""
import sys
from pathlib import Path

ROOT = Path(r"C:\Projects\CSEB")
sys.path.insert(0, str(ROOT))

from src.validation.gnucobol_runner import compile_and_run  # noqa: E402

PROGRAMS = {
    "test01": "ACCT-001: INVOICE TOTAL = 1000.00",
    "test02": "PAYROLL-001: NET PAY = 2500.00",
    "test03": "BANK-001: ACCOUNT BALANCE = 5000.00",
    "test04": "INV-001: REORDER QTY = 50 UNITS",
    "test05": "HR-001: EMPLOYEE = JOHN DOE",
    "test06": "INS-001: PREMIUM = 300.00",
    "test07": "INT-001: INTEREST EARNED = 45.50",
    "test08": "TAX-001: SALES TAX = 15.00",
    "test09": "CC-001: CARD STATUS = VALID",
    "test10": "LOAN-001: MONTHLY PAYMENT = 850.25",
}

COBOL_TEMPLATE = """\
       IDENTIFICATION DIVISION.
       PROGRAM-ID. {prog_id}.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 WS-MSG PIC X(80) VALUE '{msg}'.
       PROCEDURE DIVISION.
           DISPLAY WS-MSG.
           STOP RUN.
"""


def main() -> int:
    out_dir = ROOT / "data" / "generated" / "cobol"
    results = []

    print("=== CSEB Python Batch Validation ===")
    print(f"Programs: {len(PROGRAMS)}\n")

    for i, (name, msg) in enumerate(PROGRAMS.items(), start=1):
        source = COBOL_TEMPLATE.format(prog_id=name.upper(), msg=msg)
        r = compile_and_run(name, source, msg, out_dir)
        results.append(r)
        status = "OK  " if r.match else "FAIL"
        print(f"[{i}/{len(PROGRAMS)}] [{status}] {name}: {r.output_line!r}")

    compiled = sum(1 for r in results if r.compile.success)
    ran = sum(1 for r in results if r.run and r.run.success)
    matched = sum(1 for r in results if r.match)

    print()
    print(f"Compiled: {compiled}/{len(results)}")
    print(f"Ran:      {ran}/{len(results)}")
    print(f"Matched:  {matched}/{len(results)}")

    return 0 if matched == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())