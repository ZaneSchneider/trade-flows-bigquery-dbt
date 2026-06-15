import streamlit as st
from utils import run_query, MARTS

st.set_page_config(page_title="Country Trade Balance", layout="wide")
st.title("Country Trade Balance")
st.caption("Exports, imports, and net balance by country and year — from mart_import_export_by_country.")

df = run_query(f"""
    select iso3, country_name, year,
           export_value_thousands_usd,
           import_value_thousands_usd,
           trade_balance_thousands_usd
    from `{MARTS}.mart_import_export_by_country`
""")

year = st.slider("Year", int(df.year.min()), int(df.year.max()), int(df.year.max()))
view = df[df.year == year]
top = view.reindex(view.trade_balance_thousands_usd.abs().sort_values(ascending=False).index).head(20)

st.subheader(f"20 largest surpluses / deficits, {year}")
st.bar_chart(top.set_index("country_name")["trade_balance_thousands_usd"])
st.dataframe(view.sort_values("trade_balance_thousands_usd"), use_container_width=True)