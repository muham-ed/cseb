"""Benchmark & Leaderboard page for CSEB Dashboard."""
import json
import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(r"C:\Projects\CSEB")
DB_PATH = ROOT / "outputs" / "datasets" / "cseb.db"
LEADERBOARD_CSV = ROOT / "outputs" / "reports" / "benchmark_leaderboard.csv"
SAMPLE_TASK_JSON = ROOT / "outputs" / "reports" / "sample_benchmark_task.json"

st.header("🏆 Benchmark Tasks & LLM Leaderboard")

# Leaderboard section
st.subheader("Leaderboard")
if LEADERBOARD_CSV.exists():
    df_lb = pd.read_csv(LEADERBOARD_CSV)
    st.dataframe(df_lb, use_container_width=True)
else:
    st.info("No leaderboard CSV generated yet. Run `python scripts/run_benchmark.py`.")

st.divider()

# Benchmark tasks section
st.subheader("Benchmark Task Inspector")
if DB_PATH.exists():
    conn = sqlite3.connect(DB_PATH)
    df_tasks = pd.read_sql_query("SELECT task_id, instruction_prompt, expected_output FROM benchmark_tasks", conn)
    conn.close()

    if not df_tasks.empty:
        st.dataframe(df_tasks, use_container_width=True)

        selected_task_id = st.selectbox("Select Task ID to View Prompt & Canonical Solution", df_tasks['task_id'].tolist())

        conn = sqlite3.connect(DB_PATH)
        task_row = pd.read_sql_query(f"SELECT * FROM benchmark_tasks WHERE task_id='{selected_task_id}'", conn).iloc[0]
        conn.close()

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Instruction Prompt:**")
            st.info(task_row['instruction_prompt'])
            st.markdown("**Expected Output:**")
            st.code(task_row['expected_output'])

        with c2:
            st.markdown("**Canonical COBOL Solution:**")
            st.code(task_row['canonical_solution'], language='cobol')
