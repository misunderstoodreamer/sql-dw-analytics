"""
Streamlit analytics app for Gold-layer data warehouse.
Reads data from parquet files in data/. DB connection disabled for standalone use.
"""
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Data Warehouse Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_DIR = Path(__file__).resolve().parent / "data"
SUPPORTED_VIEWS = ["customer_reports", "product_reports"]


def load_data(view_name: str, fmt: str = "parquet"):
    """
    Load view from data/ folder (parquet or csv).
    DB connection disabled; use extract_to_local.py with .env for fresh data.

    Args:
        view_name: 'customer_reports' or 'product_reports'
        fmt: preferred format ('parquet' or 'csv')

    Returns:
        pd.DataFrame or None if file not found.
    """
    if view_name not in SUPPORTED_VIEWS:
        raise ValueError(f"Unknown view: {view_name}. Supported: {SUPPORTED_VIEWS}")

    for ext in (".parquet", ".csv") if fmt == "parquet" else (".csv", ".parquet"):
        path = DATA_DIR / f"gold.{view_name}{ext}"
        if path.exists():
            try:
                if ext == ".parquet":
                    return pd.read_parquet(path)
                return pd.read_csv(path)
            except Exception:
                continue

    return None

# --- PROFESSIONAL UI SECTION ---
st.title("DW Analytics: Presentation")
st.markdown("""
Welcome to the presentation layer of the **sql-dw-analytics** portfolio project. 
This dashboard serves as the consumption point for the implemented Modern Data Stack architecture. 

The tables below represent the **Gold Layer** (serving layer) of the Data Warehouse, built using dimensional modeling principles. To ensure a seamless, serverless deployment, the data has been extracted from the underlying MSSQL database into highly optimized `.parquet` files.
""")

st.divider()

# Load data
df_customers = load_data("customer_reports")
df_products = load_data("product_reports")

# Professional Tab Layout
tab1, tab2 = st.tabs(["Customer", "Product"])

with tab1:
    st.subheader("Customer Table")
    st.markdown("""
    Provides a consolidated, 360-degree view of customer attributes. This view is optimized for downstream Business Intelligence (BI) tools and ad-hoc analytical queries.
    """)
    
    st.markdown("**Source Extract Query:**")
    st.code("SELECT * FROM gold.customer_reports;", language="sql")
    
    if df_customers is not None:
        st.metric("Total Active Customers", f"{len(df_customers):,}")
        st.dataframe(df_customers, use_container_width=True, hide_index=True)
    else:
        st.warning("Customer data not found. Please ensure the parquet file exists in the 'data/' directory.")

with tab2:
    st.subheader("Product Table")
    st.markdown("""
    Maintains historical and current product metadata. It serves as the single source of truth for product-level performance tracking and inventory analysis.
    """)
    
    st.markdown("**Source Extract Query:**")
    st.code("SELECT * FROM gold.product_reports;", language="sql")
    
    if df_products is not None:
        st.metric("Total Products", f"{len(df_products):,}")
        st.dataframe(df_products, use_container_width=True, hide_index=True)
    else:
        st.warning("Product data not found. Please ensure the parquet file exists in the 'data/' directory.")

