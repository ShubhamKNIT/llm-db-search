import streamlit as st
from api.query_llm import get_sql_from_llm
from api.run_query import run_sql

st.set_page_config(page_title="Product Search LLM", layout="wide")
st.title("🛍️ Natural Language Product Search")

query = st.text_input("Ask for a product (e.g., 'Laptops under 60k with touch screen')")

if st.button("🔍 Search"):
    with st.spinner("Generating SQL..."):
        sql = get_sql_from_llm(query)
        st.code(sql, language="sql")

    if sql.lower().startswith("select"):
        with st.spinner("Fetching results..."):
            results = run_sql(sql)

        if not results:
            st.warning("No results found.")
        else:
            for block in results:
                st.subheader(f"Results for: `{block['query']}`")
                st.dataframe(block["rows"])
    else:
        st.error("LLM did not return a SELECT query.")
