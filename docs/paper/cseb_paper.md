# CSEB: A Legally Compliant, Verifiable Synthetic Enterprise Benchmark for COBOL AI Models

**Mohamed Alaa**  
*CSEB Research & Engineering Project*  

---

## Abstract
Legacy enterprise software written in COBOL powers over 43% of global banking systems and handles trillions of dollars in daily transactions. However, training artificial intelligence (AI) models to modernize or maintain legacy COBOL code is severely hampered by data scarcity, strict Non-Disclosure Agreements (NDAs), and legal constraints on proprietary source code. This paper presents **CSEB (COBOL Synthetic Enterprise Benchmark)**, a clean, 6-layer modular framework designed to generate, validate, enrich, and benchmark synthetic COBOL programs with 100% verified legal provenance. By leveraging native GnuCOBOL execution inside a Linux container environment, CSEB guarantees that every benchmark program is syntactically and semantically verifiable.

---

## 1. Introduction
Despite being created over six decades ago, COBOL continues to run critical infrastructure across finance, government, insurance, and supply chain management. Modernizing these systems via Large Language Models (LLMs) requires high-quality training and evaluation datasets. However, enterprise COBOL codebases are rarely accessible to researchers due to strict copyright and intellectual property restrictions.

CSEB addresses this bottleneck by providing a reproducible end-to-end framework that:
1. Generates deterministic, parametric synthetic COBOL programs across enterprise business domains.
2. Validates compilation and runtime behavior natively using GnuCOBOL 3.1.
3. Enriches code with bilingual (English/Arabic) business descriptions and McCabe cyclomatic complexity scores.
4. Provides an automated LLM evaluation harness with zero solution leakage.

---

## 2. Related Work
Existing code evaluation benchmarks such as HumanEval and MBPP focus predominantly on Python, Java, and C++. Recent efforts like CobolCodeBench have introduced COBOL tasks, but lack native integration with automated legal provenance tracking and multi-domain metadata enrichment. CSEB builds upon these concepts by adding native execution verification and bilingual documentation suitable for global enterprise applications.

---

## 3. Methodology & 6-Layer Architecture
CSEB is structured into six isolated layers:
- **Layer 1: Generation**: Parametric template-driven code synthesis.
- **Layer 2: Validation**: Native GnuCOBOL compilation and stdout exact-match verification.
- **Layer 3: Enrichment**: McCabe complexity computation, domain classification, and bilingual descriptions.
- **Layer 4: Storage**: Relational persistence in SQLite and columnar Parquet exports.
- **Layer 5: Benchmark Builder**: Standardized prompt formatting and evaluation harness.
- **Layer 6: Legal Provenance**: Automated SPDX license tracking ensuring zero IP infringement.

![Architecture](figures/fig1_architecture.png)

---

## 4. Implementation Details
The framework is implemented in Python 3.13 on Windows with native Linux execution handled via WSL Ubuntu. COBOL compilation is executed using `cobc -x -o` and validated via automated subprocess pipes. All file artifacts adhere strictly to UTF-8 without Byte Order Marks (BOM) and fixed-format COBOL column conventions starting at Column 8.

---

## 5. Experiments & Results
In our baseline experiments across 30 synthetic programs covering Accounting, Payroll, Banking, Inventory, HR, and Insurance domains:
- **Validation Rate**: 100% (30/30) compiled and produced verified output.
- **McCabe Cyclomatic Complexity**: Ranged from 1.0 to 2.0.
- **Harness Evaluation**: The dummy echo LLM baseline achieved a 100% pass rate, validating harness mechanics.

![Domain Distribution](figures/fig2_domain_distribution.png)

---

## 6. Limitations
1. Current synthetic generation relies on structured templates; future work will incorporate deep AST-level transformations.
2. Prompts are currently instruction-focused in English; multi-turn Arabic prompt evaluation remains an open direction.

---

## 7. Conclusion & Future Work
CSEB provides a robust, legally safe foundation for COBOL dataset generation and AI model evaluation. Future iterations will incorporate Java-to-COBOL cross-compilation translation verification and CICS/DB2 mainframe emulation.

---

## References
See `references.bib` for complete citation details.
