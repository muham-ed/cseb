"""Programs browser page for CSEB Dashboard."""
import json
import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(r"C:\Projects\CSEB")
DB_PATH = ROOT / "outputs" / "datasets" / "cseb.db"
ENRICHED_JSON = ROOT / "outputs" / "reports" / "enriched_v2.json"

st.header("🔍 COBOL Program Explorer")

if not DB_PATH.exists():
    st.warning("Database not found. Please run the pipeline first.")
    st.stop()

conn = sqlite3.connect(DB_PATH)
df_prog = pd.read_sql_query("SELECT * FROM cobol_programs", conn)
conn.close()

if df_prog.empty:
    st.info("No programs found.")
    st.stop()

# Filters
col_filter1, col_filter2 = st.columns(2)
with col_filter1:
    domains = ["All"] + sorted(df_prog['domain'].dropna().unique().tolist())
    selected_domain = st.selectbox("Filter by Domain", domains)

with col_filter2:
    statuses = ["All"] + sorted(df_prog['validation_status'].dropna().unique().tolist())
    selected_status = st.selectbox("Filter by Status", statuses)

filtered_df = df_prog.copy()
if selected_domain != "All":
    filtered_df = filtered_df[filtered_df['domain'] == selected_domain]
if selected_status != "All":
    filtered_df = filtered_df[filtered_df['validation_status'] == selected_status]

st.subheader(f"Programs List ({len(filtered_df)} matches)")
st.dataframe(
    filtered_df[['program_id', 'domain', 'validation_status', 'loc_count', 'complexity_score', 'created_at']],
    use_container_width=True,
)

st.divider()

# Code viewer
st.subheader("Program Source Code & Enrichment Details")
prog_ids = filtered_df['program_id'].tolist()
if prog_ids:
    selected_prog_id = st.selectbox("Select Program to Inspect", prog_ids)
    selected_row = filtered_df[filtered_df['program_id'] == selected_prog_id].iloc[0]

    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown(f"**Source Code (`{selected_prog_id}.cbl`):**")
        st.code(selected_row['generated_cobol'], language='cobol')

    with c2:
        st.markdown("**Program Metadata:**")
        st.json({
            "Program ID": selected_row['program_id'],
            "Domain": selected_row['domain'],
            "Validation Status": selected_row['validation_status'],
            "LOC": int(selected_row['loc_count']) if pd.notnull(selected_row['loc_count']) else None,
            "McCabe Complexity": float(selected_row['complexity_score']) if pd.notnull(selected_row['complexity_score']) else None,
            "License": selected_row['source_license'],
        })

        # Load description if available
        if ENRICHED_JSON.exists():
            try:
                enriched = json.loads(ENRICHED_JSON.read_text(encoding='utf-8'))
                match = next((item for item in enriched if item['program_id'] == selected_prog_id), None)
                if match:
                    st.markdown("**Business Description (English):**")
                    st.info(match.get('description_en', ''))
                    st.markdown("**الوصف التجاري (بالعربية):**")
                    st.success(match.get('description_ar', ''))
            except Exception:
                pass
