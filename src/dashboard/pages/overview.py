"""Overview page for CSEB Dashboard."""
import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(r"C:\Projects\CSEB")
DB_PATH = ROOT / "outputs" / "datasets" / "cseb.db"

st.header("📊 Dataset & Pipeline Overview")

if not DB_PATH.exists():
    st.warning("Database not found. Run `python scripts/pipeline_v3.py 30` first.")
    st.stop()

conn = sqlite3.connect(DB_PATH)
df_prog = pd.read_sql_query("SELECT * FROM cobol_programs", conn)
conn.close()

if df_prog.empty:
    st.info("No program data available in database.")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Programs by Enterprise Domain")
    domain_counts = df_prog['domain'].value_counts().reset_index()
    domain_counts.columns = ['Domain', 'Count']
    st.bar_chart(domain_counts.set_index('Domain'))

with col2:
    st.subheader("Validation Status Breakdown")
    status_counts = df_prog['validation_status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    st.bar_chart(status_counts.set_index('Status'))

st.divider()

col3, col4 = st.columns(2)

with col3:
    st.subheader("Cyclomatic Complexity Distribution")
    if 'complexity_score' in df_prog.columns:
        st.line_chart(df_prog['complexity_score'])

with col4:
    st.subheader("Lines of Code (LOC) Summary")
    if 'loc_count' in df_prog.columns:
        st.dataframe(df_prog[['program_id', 'domain', 'loc_count', 'complexity_score']].head(10), use_container_width=True)
