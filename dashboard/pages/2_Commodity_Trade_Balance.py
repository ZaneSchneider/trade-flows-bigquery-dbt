import streamlit as st
from utils import run_query, MARTS

st.set_page_config(page_title="Commodity Trade Balance", layout="wide")
st.title("Commodity Trade Balance")
st.caption("A country's commodities ranked by net balance (exports − imports) — "
           "from mart_import_export_by_product_country, labelled via dim_product.")

countries = run_query(f"""
    select distinct iso3, country_name
    from `{MARTS}.mart_import_export_by_country`
    order by country_name
""")
name_by_iso = dict(zip(countries.iso3, countries.country_name))
iso_list = list(countries.iso3)

years = run_query(f"select distinct year from `{MARTS}.mart_import_export_by_product_country` order by year")

c1, c2 = st.columns(2)
iso3 = c1.selectbox("Country", iso_list,
                    index=iso_list.index("USA") if "USA" in iso_list else 0,
                    format_func=lambda c: name_by_iso[c])
year = c2.slider("Year", int(years.year.min()), int(years.year.max()), int(years.year.max()))

df = run_query(f"""
    select
        pc.hs6_product_code,
        p.product_description,
        coalesce(pc.export_value_thousands_usd, 0) as export_value_thousands_usd,
        coalesce(pc.import_value_thousands_usd, 0) as import_value_thousands_usd,
        coalesce(pc.export_value_thousands_usd, 0)
          - coalesce(pc.import_value_thousands_usd, 0) as trade_balance_thousands_usd
    from `{MARTS}.mart_import_export_by_product_country` pc
    left join `{MARTS}.dim_product` p using (hs6_product_code)
    where pc.iso3 = '{iso3}' and pc.year = {year}
""")

top = df.reindex(df.trade_balance_thousands_usd.abs().sort_values(ascending=False).index).head(20)
top = top.assign(label=top.hs6_product_code + "  " + top.product_description.fillna(""))

st.subheader(f"{name_by_iso[iso3]} — 20 largest commodity surpluses / deficits, {year}")
st.bar_chart(top.set_index("label")["trade_balance_thousands_usd"])
st.dataframe(df.sort_values("trade_balance_thousands_usd"), use_container_width=True)