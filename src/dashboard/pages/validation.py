"""Validation & Pipeline page for CSEB Dashboard."""
import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(r"C:\Projects\CSEB")
DB_PATH = ROOT / "outputs" / "datasets" / "cseb.db"

st.header("⚡ Validation Engine & GnuCOBOL Runner")

st.markdown("""
Validation is executed inside **WSL (Ubuntu Linux)** using native **GnuCOBOL (cobc 3.1.2.0)**.
Every program undergoes:
1. Fixed-format COBOL syntax compilation.
2. Binary linking & execution.
3. Output line exact matching against deterministic expected values.
""")

if DB_PATH.exists():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT program_id, domain, validation_status, complexity_score FROM cobol_programs", conn)
    conn.close()

    total = len(df)
    passed = len(df[df['validation_status'] == 'passed'])
    failed = total - passed

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Executed", total)
    col2.metric("Passed (100% Match)", passed)
    col3.metric("Failed / Errors", failed)

    st.subheader("Validation Status Table")
    st.dataframe(df, use_container_width=True)
else:
    st.info("No validation data available.")
