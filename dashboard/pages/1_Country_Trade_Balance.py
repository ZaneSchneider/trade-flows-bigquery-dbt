import streamlit as st
from utils import run_query, MARTS
import altair as alt

st.set_page_config(page_title="Country Trade Balance", layout="wide")
st.title("Country Trade Balance")
st.caption("Exports, imports, and net balance by country and year — from mart_trade_by_country.")

df = run_query(f"""
    select iso3, country_name, year,
           export_value_thousands_usd,
           import_value_thousands_usd,
           trade_balance_thousands_usd
    from `{MARTS}.mart_trade_by_country`
""")

year = st.slider("Year", int(df.year.min()), int(df.year.max()), int(df.year.max()))
view = df[df.year == year]
top = (view.reindex(view.trade_balance_thousands_usd.abs().sort_values(ascending=False).index)
           .head(20)
           .sort_values("trade_balance_thousands_usd", ascending=False))

st.subheader(f"20 largest surpluses / deficits, {year}")
st.altair_chart(
    alt.Chart(top).mark_bar().encode(
        y=alt.Y("country_name:N", sort="-x", title=None),
        x=alt.X("trade_balance_thousands_usd:Q", title="Trade balance (USD thousands)"),
    ),
    use_container_width=True,
)
NICE = {
    "iso3": "ISO3",
    "country_name": "Country",
    "year": "Year",
    "export_value_thousands_usd": "Exports (USD thousands)",
    "import_value_thousands_usd": "Imports (USD thousands)",
    "trade_balance_thousands_usd": "Trade Balance (USD thousands)",
}
st.dataframe(view.sort_values("trade_balance_thousands_usd").rename(columns=NICE), use_container_width=True)