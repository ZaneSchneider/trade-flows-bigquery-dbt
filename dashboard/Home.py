import streamlit as st
from utils import run_query, MARTS

st.set_page_config(page_title="Trade Flow V2", layout="wide")
st.title("Trade Flow — V2")
st.caption("BACI HS92 bilateral trade · GCS → BigQuery → dbt · self-engineered pipeline")
st.markdown("Descriptive views over a self-built pipeline. Use the sidebar pages.")

with st.expander("Connection check"):
    df = run_query(f"select table_name from `{MARTS}`.INFORMATION_SCHEMA.TABLES order by table_name")
    st.write(f"Connected — {len(df)} tables in the marts dataset:")
    st.dataframe(df, use_container_width=True)