import streamlit as st
from utils import run_query, MARTS

st.set_page_config(page_title="Top Traded Products", layout="wide")
st.title("Top Traded Products")
st.caption("World trade value by commodity (HS6) — from mart_trade_by_product.")

df = run_query(f"""
    select hs6_product_code, year, product_description, trade_value_thousands_usd
    from `{MARTS}.mart_trade_by_product`
""")

year = st.slider("Year", int(df.year.min()), int(df.year.max()), int(df.year.max()))
view = df[df.year == year].nlargest(25, "trade_value_thousands_usd")
view = view.assign(label=view.hs6_product_code + "  " + view.product_description.fillna(""))

st.subheader(f"25 most-traded commodities worldwide, {year}")
st.bar_chart(view.set_index("label")["trade_value_thousands_usd"])
st.dataframe(
    view[["hs6_product_code", "product_description", "trade_value_thousands_usd"]],
    use_container_width=True,
)

st.subheader("World trade over time")
prods = df[["hs6_product_code", "product_description"]].drop_duplicates().sort_values("product_description")
name_by_code = dict(zip(prods.hs6_product_code, prods.product_description))
code_list = list(prods.hs6_product_code)
top_code = df.groupby("hs6_product_code")["trade_value_thousands_usd"].sum().idxmax()
code = st.selectbox("Commodity", code_list,
                    index=code_list.index(top_code),
                    format_func=lambda c: f"{c}  {name_by_code[c]}")
trend = df[df.hs6_product_code == code].sort_values("year")
st.line_chart(trend.set_index("year")["trade_value_thousands_usd"])