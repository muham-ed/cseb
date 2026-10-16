"""Unit tests for GnuCOBOL runner module."""
from __future__ import annotations

from pathlib import Path
import pytest

from src.validation.gnucobol_runner import (
    windows_to_wsl_path,
    write_cobol_source,
    compile_cobol,
    compile_and_run,
)


def test_windows_to_wsl_path():
    """Test Windows to WSL path conversion."""
    p1 = windows_to_wsl_path(r"C:\foo\bar")
    assert p1 == "/mnt/c/foo/bar"

    p2 = windows_to_wsl_path(r"C:\Projects\CSEB")
    assert p2 == "/mnt/c/Projects/CSEB"


def test_write_cobol_source_lf_no_bom(tmp_path: Path):
    """Test that write_cobol_source writes UTF-8 without BOM using LF newlines."""
    cbl = tmp_path / "test.cbl"
    source = "       IDENTIFICATION DIVISION.\r\n       PROGRAM-ID. TEST.\r\n"
    write_cobol_source(cbl, source)

    raw_bytes = cbl.read_bytes()
    # Check no UTF-8 BOM (EF BB BF)
    assert not (len(raw_bytes) >= 3 and raw_bytes[:3] == b"\xef\xbb\xbf")
    # Check LF line endings, no CR (\r)
    assert b"\r" not in raw_bytes
    assert b"\n" in raw_bytes


def test_compile_and_run_success(tmp_path: Path):
    """Test compiling and running a valid COBOL program via WSL GnuCOBOL."""
    valid_cobol = """\
       IDENTIFICATION DIVISION.
       PROGRAM-ID. TINY.
       PROCEDURE DIVISION.
           DISPLAY 'TINY OK'.
           STOP RUN.
"""
    res = compile_and_run(
        name="tiny_test",
        source=valid_cobol,
        expected="TINY OK",
        out_dir=tmp_path,
    )
    assert res.compile.success is True
    assert res.run is not None
    assert res.run.success is True
    assert res.output_line == "TINY OK"
    assert res.match is True


def test_compile_failure_invalid_cobol(tmp_path: Path):
    """Test that invalid COBOL produces compile failure."""
    invalid_cobol = "THIS IS NOT VALID COBOL CODE AT ALL"
    cbl_path = tmp_path / "invalid.cbl"
    write_cobol_source(cbl_path, invalid_cobol)

    comp = compile_cobol(cbl_path)
    assert comp.success is False
    assert comp.exit_code != 0
