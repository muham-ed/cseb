"""GnuCOBOL compiler and runtime wrapper via WSL.

All COBOL compilation and execution happens inside WSL (Ubuntu) where
GnuCOBOL 3.x is installed. Windows paths are translated to /mnt/c/...
before being passed to WSL.
"""
from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class CompileResult:
    success: bool
    cbl_path: Path
    exe_path: Path
    exit_code: int
    stdout: str
    stderr: str
    wsl_cbl: str
    wsl_exe: str


@dataclass
class RunResult:
    success: bool
    exe_path: Path
    exit_code: int
    stdout: str
    stderr: str


@dataclass
class PipelineResult:
    name: str
    compile: CompileResult
    run: Optional[RunResult]
    output_line: str
    expected_output: str
    match: bool


def windows_to_wsl_path(win_path) -> str:
    """Convert C:\\foo\\bar -> /mnt/c/foo/bar."""
    p = Path(win_path)
    if not p.is_absolute():
        p = p.resolve()
    drive = p.drive.rstrip(":").lower()
    if not drive:
        raise ValueError(f"Cannot convert non-absolute path: {win_path}")
    parts = p.parts[1:]  # skip "C:\\"
    joined = "/".join(parts).replace("\\", "/")
    return f"/mnt/{drive}/{joined}"


def write_cobol_source(cbl_path: Path, source: str) -> None:
    """Write COBOL source as UTF-8 no BOM with LF newlines (GnuCOBOL requirement)."""
    cbl_path = Path(cbl_path)
    cbl_path.parent.mkdir(parents=True, exist_ok=True)
    normalized = source.replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.endswith("\n"):
        normalized += "\n"
    cbl_path.write_text(normalized, encoding="utf-8", newline="\n")


def compile_cobol(cbl_path: Path, retries: int = 2) -> CompileResult:
    """Compile a .cbl file to a native executable via GnuCOBOL inside WSL with retry logic."""
    cbl_path = Path(cbl_path)
    exe_path = cbl_path.with_suffix("")
    wsl_cbl = windows_to_wsl_path(cbl_path)
    wsl_exe = windows_to_wsl_path(exe_path)

    for attempt in range(retries + 1):
        proc = subprocess.run(
            ["wsl", "cobc", "-x", "-o", wsl_exe, wsl_cbl],
            capture_output=True,
            text=True,
        )
        if proc.returncode == 0 or attempt == retries:
            break
        time.sleep(0.5)

    return CompileResult(
        success=(proc.returncode == 0),
        cbl_path=cbl_path,
        exe_path=exe_path,
        exit_code=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
        wsl_cbl=wsl_cbl,
        wsl_exe=wsl_exe,
    )


def run_cobol(exe_path: Path) -> RunResult:
    """Run a previously compiled COBOL executable inside WSL."""
    exe_path = Path(exe_path)
    wsl_exe = windows_to_wsl_path(exe_path)
    proc = subprocess.run(
        ["wsl", wsl_exe],
        capture_output=True,
        text=True,
    )
    return RunResult(
        success=(proc.returncode == 0),
        exe_path=exe_path,
        exit_code=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
    )


def compile_and_run(
    name: str,
    source: str,
    expected: str,
    out_dir: Path,
) -> PipelineResult:
    """Full pipeline: write source -> compile -> run -> compare output."""
    cbl_path = Path(out_dir) / f"{name}.cbl"
    write_cobol_source(cbl_path, source)

    comp = compile_cobol(cbl_path)
    run: Optional[RunResult] = None
    output_line = ""

    if comp.success:
        run = run_cobol(comp.exe_path)
        output_line = run.stdout.strip()

    return PipelineResult(
        name=name,
        compile=comp,
        run=run,
        output_line=output_line,
        expected_output=expected,
        match=(output_line == expected),
    )
