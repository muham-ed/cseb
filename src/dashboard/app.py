"""Streamlit Dashboard Entry Point for CSEB."""
from __future__ import annotations

import sqlite3
import pandas as pd
import streamlit as st
from pathlib import Path

ROOT = Path(r"C:\Projects\CSEB")
DB_PATH = ROOT / "outputs" / "datasets" / "cseb.db"

st.set_page_config(
    page_title="CSEB — COBOL Benchmark Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555555;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #1E88E5;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">CSEB — COBOL Synthetic Enterprise Benchmark</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">A legally compliant, verifiable benchmark pipeline for LLMs & Legacy COBOL Data</div>', unsafe_allow_html=True)

st.sidebar.image("https://img.icons8.com/color/96/code.png", width=64)
st.sidebar.title("Navigation")
st.sidebar.info("Use the sidebar pages to navigate through CSEB analytics, program inspection, and benchmark leaderboards.")

# --- Quick Stats ---
if DB_PATH.exists():
    conn = sqlite3.connect(DB_PATH)
    try:
        df_prog = pd.read_sql_query("SELECT * FROM cobol_programs", conn)
        df_tasks = pd.read_sql_query("SELECT * FROM benchmark_tasks", conn)
    except Exception:
        df_prog = pd.DataFrame()
        df_tasks = pd.DataFrame()
    conn.close()
else:
    df_prog = pd.DataFrame()
    df_tasks = pd.DataFrame()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Generated Programs", value=len(df_prog) if not df_prog.empty else 0)

with col2:
    passed = len(df_prog[df_prog['validation_status'] == 'passed']) if not df_prog.empty else 0
    total = len(df_prog) if not df_prog.empty else 1
    rate = (passed / total) * 100 if total > 0 else 0
    st.metric(label="GnuCOBOL Validation Rate", value=f"{rate:.1f}%")

with col3:
    st.metric(label="Benchmark Tasks Built", value=len(df_tasks) if not df_tasks.empty else 0)

with col4:
    domains_count = df_prog['domain'].nunique() if not df_prog.empty and 'domain' in df_prog.columns else 0
    st.metric(label="Active Enterprise Domains", value=domains_count)

st.divider()

st.subheader("System Architecture & Pipeline Flow")
st.markdown("""
- **Layer 1 (Generation)**: Parametric synthetic generation from structured business templates.
- **Layer 2 (Validation)**: Native GnuCOBOL 3.1 compiler execution inside WSL Ubuntu.
- **Layer 3 (Enrichment)**: McCabe cyclomatic complexity, domain classification, and bilingual descriptions (EN/AR).
- **Layer 4 (Storage)**: Relational SQLite (`cseb.db`) & Parquet datasets.
- **Layer 5 (Benchmark Builder)**: Standardized LLM prompts and task specifications (CSEB benchmark suite).
- **Layer 6 (Legal Provenance)**: 100% clean synthetic data provenance without leaked IP or NDA constraints.
""")

st.info("👈 Select a page from the sidebar on the left to view detailed charts, program code, or benchmark leaderboards for your presentation!")
