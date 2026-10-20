# CSEB — COBOL Synthetic Enterprise Benchmark

> Status as of October 2026. Every claim in this report is verifiable
> through the open repository and local test runs.

## Overview
CSEB is an open-source pipeline that generates synthetic COBOL-85 programs,
verifies each one by actually compiling and running it via GnuCOBOL 3.1
inside WSL, enriches them with metadata and bilingual descriptions, and
exposes an evaluation harness for benchmarking LLMs on COBOL tasks.

Current stage: Proof of Concept — 31 programs generated and validated.

## Architecture — 6 layers

1. **Generation**: Parameterized COBOL-85 templates (DISPLAY, ADDITION, CONDITIONAL).
2. **Validation**: Real compile + run via GnuCOBOL 3.1 (31/31 = 100%).
3. **Enrichment**: McCabe complexity, domain classification, AR+EN descriptions
   (rule-based, not LLM).
4. **Storage**: SQLite + export to JSONL, Parquet, SQLite.
5. **Benchmark**: Evaluation harness accepting any LLM callable (pass@1, compile_rate).
6. **Legal Provenance**: Schema + SPDX scanner ready. Table currently empty (0 rows).

## Key features

- **Bilingual** AR + EN descriptions (rule-based, template-mapped).
- **MIT license** — free for commercial use.
- **Executable validation**, not static checking.
- **Streamlit dashboard** (single-page, 5 sections via sidebar).
- **FastAPI** endpoints: /stats, /programs, /benchmarks, /legal/{id}.
- **Pytest**: 16 tests passing, **61% coverage** (not 100%).

## Current state (verified)

| Item | Value |
|---|---|
| COBOL programs in DB | 31 |
| GnuCOBOL validation rate | 31/31 (100%) |
| Benchmark tasks ready | 31 |
| Pytest tests | 16 passing, 61% coverage |
| Real LLM evaluation | **NOT RUN YET** (needs Ollama) |
| legal_provenance records | **0** (schema ready, audit pending) |
| Dataset export size | 31 records in JSONL / Parquet / SQLite |

## Roadmap

**Short term (next):**
1. Install Ollama + run `benchmark_with_llm.py` on qwen2.5-coder:7b
   for first real LLM evaluation.
2. Populate `legal_provenance` with SPDX audit per program.
3. Expand templates to include PERFORM, EVALUATE, FILE SECTION.
4. Generate 1,000 programs as first scale-up.

**Medium term:**
- Java→COBOL translation via LLM.
- EXEC SQL / EXEC CICS support (syntactic; runtime testing needs emulators).
- HuggingFace Datasets publication.

## Anti-claims (do not publish as true)
- NOT 500k lines — 31 programs, ~2,400 lines total.
- NOT "first global bilingual benchmark" — no verifiable basis.
- NOT "100% test coverage" — 61%.
- NOT comparing OpenAI vs Anthropic vs Ollama — harness only, no runs.
- NOT "SHA256 signature per program" — schema exists, not populated.
- NOT "EXEC SQL / CICS / VSAM / COPYBOOKS verified" — no such templates yet.