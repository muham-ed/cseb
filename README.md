# CSEB — COBOL Synthetic Enterprise Benchmark

![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)
![GnuCOBOL 3.1](https://img.shields.io/badge/GnuCOBOL-3.1.2-green.svg)
![Tests Passing](https://img.shields.io/badge/Pytest-100%25--Passing-brightgreen.svg)
![License MIT](https://img.shields.io/badge/License-MIT-orange.svg)

**CSEB** is a clean, 6-layer modular framework for generating, validating, enriching, and benchmarking synthetic COBOL programs with 100% verified legal provenance.

---

## 🏗️ Architecture (6 Layers)

1. **Layer 1 (Generation)**: Parametric template-driven synthesis across 6 enterprise domains (Accounting, Payroll, Banking, Inventory, HR, Insurance).
2. **Layer 2 (Validation)**: Native GnuCOBOL 3.1 execution engine inside WSL Ubuntu with exact stdout comparison.
3. **Layer 3 (Enrichment)**: McCabe cyclomatic complexity, domain classification, and bilingual (English/Arabic) business descriptions.
4. **Layer 4 (Storage & Datasets)**: Relational SQLite database (`cseb.db`) and exports to JSONL, Parquet, and standalone SQLite.
5. **Layer 5 (Benchmark Builder)**: Standardized LLM prompt evaluation harness with automated model leaderboard.
6. **Layer 6 (Legal Provenance)**: Automated SPDX license auditing ensuring zero IP infringement or NDA leaks.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Full End-to-End Pipeline
```bash
python scripts/pipeline_v3.py 30
```

### 3. Run Benchmark Harness
```bash
python scripts/run_benchmark.py
```

### 4. Launch Interactive Streamlit Dashboard
```bash
streamlit run src/dashboard/app.py
```

### 5. Launch FastAPI Documentation Server
```bash
uvicorn src.api.main:app --reload
```

---

## 🧪 Run Test Suite

```bash
python -m pytest tests/ -v --cov=src
```

---

## 📄 Citation

```bibtex
@article{cseb2026,
  title={CSEB: A Legally Compliant, Verifiable Synthetic Enterprise Benchmark for COBOL AI Models},
  author={Alaa, Mohamed},
  year={2026}
}
```
