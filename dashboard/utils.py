from pathlib import Path
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

PROJECT = "trade-flow-analysis"
MARTS = "trade-flow-analysis.trade_flow_v2_marts"
KEYFILE = Path(__file__).resolve().parents[1] / "secrets" / "baci-fetcher-key.json"

@st.cache_resource
def get_client():
    """One shared BigQuery client (cache_resource = one object, reused across reruns)."""
    creds = service_account.Credentials.from_service_account_file(str(KEYFILE))
    return bigquery.Client(credentials=creds, project=PROJECT)

@st.cache_data(ttl=3600)
def run_query(sql: str):
    """Run SQL -> DataFrame. Result cached 1h (cache_data = cached copy keyed on the SQL)."""
    return get_client().query(sql).to_dataframe()