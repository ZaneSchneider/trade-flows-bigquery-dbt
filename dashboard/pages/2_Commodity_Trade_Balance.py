import streamlit as st
import altair as alt
from utils import run_query, MARTS

st.set_page_config(page_title="Commodity Trade Balance", layout="wide")
st.title("Commodity Trade Balance")
st.caption("A country's commodities ranked by net balance (exports − imports) — "
           "from mart_trade_by_country_product, labelled via dim_product.")

countries = run_query(f"""
    select distinct country_code, iso3, country_name
    from `{MARTS}.mart_trade_by_country`
    order by country_name
""")
name_by_code = dict(zip(countries.country_code, countries.country_name))
code_list = list(countries.country_code)
usa = countries.loc[countries.iso3 == "USA", "country_code"]
default_index = code_list.index(usa.iloc[0]) if len(usa) else 0

years = run_query(f"select distinct year from `{MARTS}.mart_trade_by_country_product` order by year")

c1, c2 = st.columns(2)
code = c1.selectbox("Country", code_list,
                    index=default_index,
                    format_func=lambda c: name_by_code[c])
year = c2.slider("Year", int(years.year.min()), int(years.year.max()), int(years.year.max()))

df = run_query(f"""
    select
        pc.hs6_product_code,
        p.product_description,
        coalesce(pc.export_value_thousands_usd, 0) as export_value_thousands_usd,
        coalesce(pc.import_value_thousands_usd, 0) as import_value_thousands_usd,
        coalesce(pc.export_value_thousands_usd, 0)
          - coalesce(pc.import_value_thousands_usd, 0) as trade_balance_thousands_usd
    from `{MARTS}.mart_trade_by_country_product` pc
    left join `{MARTS}.dim_product` p using (hs6_product_code)
    where pc.country_code = {code} and pc.year = {year}
""")

top = (df.reindex(df.trade_balance_thousands_usd.abs().sort_values(ascending=False).index)
         .head(20))
top = top.assign(label=top.hs6_product_code + "  " + top.product_description.fillna(""))

st.subheader(f"{name_by_code[code]} — 20 largest commodity surpluses / deficits, {year}")
st.altair_chart(
    alt.Chart(top).mark_bar().encode(
        y=alt.Y("label:N", sort="-x", title=None),
        x=alt.X("trade_balance_thousands_usd:Q", title="Trade balance (USD thousands)"),
    ),
    use_container_width=True,
)
NICE = {
    "hs6_product_code": "HS6",
    "product_description": "Product",
    "export_value_thousands_usd": "Exports (USD thousands)",
    "import_value_thousands_usd": "Imports (USD thousands)",
    "trade_balance_thousands_usd": "Trade Balance (USD thousands)",
}
st.dataframe(df.sort_values("trade_balance_thousands_usd").rename(columns=NICE), use_container_width=True)