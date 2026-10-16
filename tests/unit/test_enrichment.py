"""Unit tests for enrichment module (complexity, domain, metadata, descriptions)."""
from __future__ import annotations

from src.enrichment.complexity_analyzer import analyze_complexity
from src.enrichment.domain_classifier import classify_domain
from src.enrichment.metadata_extractor import extract_metadata
from src.enrichment.business_describer import describe


def test_complexity_analyzer():
    """Test McCabe cyclomatic complexity calculation."""
    simple = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. SIMPLE.
       PROCEDURE DIVISION.
           DISPLAY 'HELLO'.
           STOP RUN.
    """
    assert analyze_complexity(simple) == 1.0

    conditional = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. COND.
       PROCEDURE DIVISION.
           IF A > B
               DISPLAY 'YES'
           ELSE
               DISPLAY 'NO'
           END-IF.
           STOP RUN.
    """
    assert analyze_complexity(conditional) == 2.0


def test_domain_classifier():
    """Test keyword-based domain classification."""
    code_acc = "01 WS-MSG PIC X VALUE 'INVOICE TOTAL'."
    assert classify_domain(code_acc) == "accounting"

    code_pay = "01 WS-MSG PIC X VALUE 'NET PAYROLL SALARY'."
    assert classify_domain(code_pay) == "payroll"

    code_bank = "01 WS-MSG PIC X VALUE 'ACCOUNT BANK BALANCE'."
    assert classify_domain(code_bank) == "banking"


def test_metadata_extractor():
    """Test metadata extraction from COBOL code."""
    sample = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. SAMPLE01.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 WS-A PIC 9(5)V99 VALUE 10.00.
       01 WS-B PIC X(20) VALUE 'TEST'.
       PROCEDURE DIVISION.
           STOP RUN.
    """
    meta = extract_metadata(sample)
    assert meta["program_id"] == "SAMPLE01"
    assert meta["loc"] > 0
    assert "9(5)V99" in meta["pic_types"]
    assert "IDENTIFICATION" in meta["divisions"]


def test_business_describer():
    """Test English and Arabic business descriptions."""
    desc_en = describe("", language="en", template_name="ADDITION")
    assert "Adds two numeric fields" in desc_en

    desc_ar = describe("", language="ar", template_name="ADDITION")
    assert "يجمع حقلين" in desc_ar
