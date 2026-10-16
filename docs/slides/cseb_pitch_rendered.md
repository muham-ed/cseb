---
marp: true
theme: default
paginate: true
header: 'CSEB Pitch Deck'
footer: '© 2026 CSEB Project'
---

# CSEB: COBOL Synthetic Enterprise Benchmark
### Legal-Clean Synthetic Data & Verifiable AI Benchmark for Legacy Modernization

**Mohamed Alaa** | Founder & Lead Architect

---

## The Problem
- **COBOL Powers the World**: 43% of banking systems and 95% of ATM transactions run on COBOL.
- **The Talent Gap**: 92% of modern developers cannot read or maintain COBOL.
- **The Data Wall**: Enterprise COBOL code is locked behind strict NDAs and copyright law.
- **AI Models Fail**: Off-the-shelf LLMs hallucinate syntax and leak proprietary code.

---

## The Solution
- **CSEB Framework**: A clean 6-layer pipeline for generating 100% legal synthetic COBOL.
- **Compiler Verifiable**: Every program is compiled and executed via native GnuCOBOL 3.1.
- **Bilingual Documentation**: Automated English & Arabic business descriptions.
- **Zero IP Leakage**: 100% clean provenance with permissive MIT licensing.

---

## Pipeline Architecture
1. **Generation**: Parametric business logic synthesis.
2. **Validation**: Native GnuCOBOL execution inside Linux containers.
3. **Enrichment**: McCabe complexity & bilingual documentation.
4. **Storage**: Relational SQLite & Parquet dataset export.
5. **Benchmark**: Standardized LLM prompt evaluation harness.
6. **Legal**: Automated SPDX license provenance audit.

---

## Live System Numbers
- **Total Generated Programs**: 31
- **GnuCOBOL Pass Rate**: 100.0%
- **Active Domains**: 7 (Accounting, Payroll, Banking, HR, Insurance)
- **Benchmark Tasks Built**: 31

---

## Enterprise Domain Coverage
- **Accounting**: Invoices, general ledgers, tax calculation.
- **Payroll**: Net pay, wage deductions, salary slips.
- **Banking**: Account balances, deposit/withdrawal calculations.
- **Inventory**: Stock counts, reorder thresholds, warehouse tracking.
- **HR & Insurance**: Employee records and premium estimations.

---

## Evaluation Benchmark Methodology
- **Instruction Prompts**: Clear, English business specifications.
- **Execution Verification**: LLM-generated code is compiled and executed against exact expected output.
- **Metrics Computed**: Pass@1 match rate, compilation pass rate, and cyclomatic complexity delta.

---

## LLM Leaderboard Summary
- **Baseline Harness**: Tested & verified with 100% pass rate.
- **Local Models Supported**: Seamless integration with Ollama (Qwen2.5-Coder, Llama-3, DeepSeek-Coder).
- **Automated Leaderboard**: Exported directly to CSV and Streamlit Dashboard.

---

## Dataset Formats & Commercial Export
- **JSONL**: Lightweight line-delimited records for LLM fine-tuning.
- **Parquet**: Columnar format for high-speed PyTorch / HuggingFace data loaders.
- **SQLite**: Standalone relational database for SQL analytics.

---

## Legal Provenance & Compliance
- **100% Synthetic**: No NDA violations, zero bank source leaks.
- **Clean License Lineage**: Full audit trail for commercial AI model licensing.
- **Enterprise Safe**: Compliant with international data licensing standards.

---

## Strategic Roadmap
- **Q1 2026**: Template pipeline scaling to 100,000+ verified programs.
- **Q2 2026**: Java / C# to COBOL cross-compilation translation layer.
- **Q3 2026**: Mainframe DB2 & CICS transaction emulation.

---

# Thank You!
### CSEB — Building the Future of Legacy System Modernization

**Contact**: Mohamed Alaa  
**Dashboard**: `http://localhost:8501`  
**API Docs**: `http://localhost:8000/docs`
