from pathlib import Path
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

PROJECT = "trade-flow-analysis"
MARTS = "trade-flow-analysis.trade_flow_v2_marts"
KEYFILE = Path(__file__).resolve().parents[1] / "secrets" / "baci-fetcher-key.json"
CAP_BYTES = 2 * 1024**3  # 2 GiB ceiling per query

@st.cache_resource
def get_client():
    """One shared BigQuery client. st.secrets on Cloud, local key file otherwise."""
    if "gcp_service_account" in st.secrets:
        creds = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
    else:
        creds = service_account.Credentials.from_service_account_file(str(KEYFILE))
    return bigquery.Client(credentials=creds, project=PROJECT)

@st.cache_data(ttl=3600)
def run_query(sql: str):
    job_config = bigquery.QueryJobConfig(maximum_bytes_billed=CAP_BYTES)
    return get_client().query(sql, job_config=job_config).to_dataframe()