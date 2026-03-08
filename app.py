"""
Streamlit analytics app for Gold-layer data warehouse.
Reads data from parquet files in data/. DB connection disabled for standalone use.
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="DW Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main { background-color: #0f1117; }

    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1e2130, #252a3a);
        border: 1px solid #2e3450;
        border-radius: 12px;
        padding: 16px 20px;
    }
    [data-testid="metric-container"] label {
        color: #8b92a8 !important;
        font-size: 0.78rem !important;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #e8ecf4 !important;
        font-size: 1.6rem !important;
        font-weight: 700;
    }

    hr { border-color: #2e3450 !important; margin: 1.5rem 0; }

    /* Page title & subheadings — main content only, sidebar excluded */
    .main h1 {
        color: #111827 !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.01em;
    }

    .main h2, .main h3 {
        color: #1e293b !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
    }

    .section-label {
        color: #e6e6e6;
        font-size: 0.72rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .filter-note {
        color: #e6e6e6;
        font-size: 0.70rem;
        font-style: italic;
        margin-top: -4px;
        margin-bottom: 8px;
    }

    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background: #1e2130;
        border-radius: 8px;
        color: #8b92a8;
        padding: 8px 20px;
        border: 1px solid #2e3450;
    }
    .stTabs [aria-selected="true"] {
        background: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
    }

    .stDataFrame { border-radius: 10px; overflow: hidden; }

    section[data-testid="stSidebar"] {
        background-color: #13151f;
        border-right: 1px solid #2e3450;
    }
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #8b92a8;
        font-size: 0.72rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 2px;
    }
</style>
""", unsafe_allow_html=True)

DATA_DIR = Path(__file__).resolve().parent / "data"
SUPPORTED_VIEWS = ["customer_reports", "product_reports"]

SEGMENT_COLORS = {
    "VIP": "#f59e0b",
    "REGULAR": "#3b82f6",
    "NEW": "#10b981",
    "High-Performer": "#f59e0b",
    "Mid-Range": "#3b82f6",
    "Low-Performer": "#6b7280",
}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#c5cad8", family="Inter, sans-serif", size=12),
    margin=dict(l=10, r=10, t=36, b=10),
    showlegend=True,
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    xaxis=dict(gridcolor="#2e3450", linecolor="#2e3450", tickfont=dict(size=11)),
    yaxis=dict(gridcolor="#2e3450", linecolor="#2e3450", tickfont=dict(size=11)),
)

AGE_ORDER = ["Under 20", "Under 20-29", "Under 30-39", "Under 40-49", "50 and Above"]


def load_data(view_name: str, fmt: str = "parquet") -> pd.DataFrame | None:
    if view_name not in SUPPORTED_VIEWS:
        raise ValueError(f"Unknown view: {view_name}. Supported: {SUPPORTED_VIEWS}")
    for ext in (".parquet", ".csv") if fmt == "parquet" else (".csv", ".parquet"):
        path = DATA_DIR / f"gold.{view_name}{ext}"
        if path.exists():
            try:
                return pd.read_parquet(path) if ext == ".parquet" else pd.read_csv(path)
            except Exception:
                continue
    return None


def plotly_bar(df_series: pd.Series, title: str, color_map: dict | None = None,
               horizontal: bool = False, color_single: str = "#3b82f6") -> None:
    df = df_series.reset_index()
    df.columns = ["label", "value"]
    colors = [color_map.get(v, color_single) for v in df["label"]] if color_map else color_single

    if horizontal:
        fig = px.bar(df, x="value", y="label", orientation="h", title=title,
                     color="label", color_discrete_map=color_map or {})
    else:
        fig = px.bar(df, x="label", y="value", title=title,
                     color="label", color_discrete_map=color_map or {})

    fig.update_layout(**PLOTLY_LAYOUT, title=dict(text=title, font=dict(size=16, color="#000000")))
    fig.update_traces(marker_color=colors if not color_map else None)
    st.plotly_chart(fig, use_container_width=True)


def plotly_pie(df_series: pd.Series, title: str, color_map: dict | None = None) -> None:
    df = df_series.reset_index()
    df.columns = ["label", "value"]
    colors = [color_map.get(v, "#3b82f6") for v in df["label"]] if color_map else None
    fig = px.pie(df, names="label", values="value", title=title,
                 color="label", color_discrete_map=color_map or {}, hole=0.45)
    fig.update_layout(**{k: v for k, v in PLOTLY_LAYOUT.items() if k not in ("xaxis", "yaxis")},
                      title=dict(text=title, font=dict(size=16, color="#000000")))
    if colors:
        fig.update_traces(marker=dict(colors=colors), textfont=dict(color="#ffffff"))
    st.plotly_chart(fig, use_container_width=True)


# ── Load raw data ─────────────────────────────────────────────────────────────
df_customers = load_data("customer_reports")
df_products = load_data("product_reports")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("Filters")
    st.markdown('<p class="filter-note">Affects KPIs and table only.<br>Charts always show the full dataset.</p>',
                unsafe_allow_html=True)

    st.divider()

    # ── Customer filters ──────────────────────────────────────────────────────
    st.markdown("### Customer")

    if df_customers is not None:
        sel_cust_seg = st.multiselect(
            "Segment",
            options=["VIP", "REGULAR", "NEW"],
            default=[],
            key="cust_seg",
            placeholder="All segments",
        )
        sel_cust_age = st.multiselect(
            "Age Group",
            options=[a for a in AGE_ORDER if a in df_customers["age_group"].unique()],
            default=[],
            key="cust_age",
            placeholder="All age groups",
        )
    else:
        sel_cust_seg, sel_cust_age = [], []

    st.divider()

    # ── Product filters ───────────────────────────────────────────────────────
    st.markdown("### Product")

    if df_products is not None:
        all_cats = sorted(df_products["category"].dropna().unique())
        sel_prod_cat = st.multiselect(
            "Category",
            options=all_cats,
            default=[],
            key="prod_cat",
            placeholder="All categories",
        )

        # Cascading: subcategory pool narrows when category is selected
        subcat_pool = (
            df_products[df_products["category"].isin(sel_prod_cat)]["subcategory"].dropna().unique()
            if sel_prod_cat
            else df_products["subcategory"].dropna().unique()
        )
        sel_prod_subcat = st.multiselect(
            "Subcategory",
            options=sorted(subcat_pool),
            default=[],
            key="prod_subcat",
            placeholder="All subcategories",
        )

        sel_prod_seg = st.multiselect(
            "Segment",
            options=["High-Performer", "Mid-Range", "Low-Performer"],
            default=[],
            key="prod_seg",
            placeholder="All segments",
        )
    else:
        sel_prod_cat, sel_prod_subcat, sel_prod_seg = [], [], []

    # st.divider()
    # if st.button("Reset All Filters", use_container_width=True):
    #     for key in ("cust_seg", "cust_age", "prod_cat", "prod_subcat", "prod_seg"):
    #         if key in st.session_state:
    #             del st.session_state[key]
    #     st.rerun()

# ── Apply filters ─────────────────────────────────────────────────────────────
df_cust_f = df_customers.copy() if df_customers is not None else None
if df_cust_f is not None:
    if sel_cust_seg:
        df_cust_f = df_cust_f[df_cust_f["customer_segment"].isin(sel_cust_seg)]
    if sel_cust_age:
        df_cust_f = df_cust_f[df_cust_f["age_group"].isin(sel_cust_age)]

df_prod_f = df_products.copy() if df_products is not None else None
if df_prod_f is not None:
    if sel_prod_cat:
        df_prod_f = df_prod_f[df_prod_f["category"].isin(sel_prod_cat)]
    if sel_prod_subcat:
        df_prod_f = df_prod_f[df_prod_f["subcategory"].isin(sel_prod_subcat)]
    if sel_prod_seg:
        df_prod_f = df_prod_f[df_prod_f["product_segment"].isin(sel_prod_seg)]

# ── Header ────────────────────────────────────────────────────────────────────
st.title("DW Analytics")
st.markdown("""
Presentation layer of the **sql-dw-analytics** portfolio project — consumption point for a Modern Data Stack
built on **Star Schema** dimensional modeling. Data is served from the Gold Layer via optimized `.parquet` files.
""")
st.divider()

tab1, tab2 = st.tabs(["Customer", "Product"])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — CUSTOMER
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Customer Report")
    st.markdown("""
    360-degree customer view with age segmentation, recency, average order value and
    monthly spend — mirroring the `gold.customer_reports` analytical view.
    """)
    st.code("SELECT * FROM gold.customer_reports;", language="sql")

    if df_customers is not None:
        # KPIs from filtered data
        seg_counts_f = df_cust_f["customer_segment"].value_counts()
        is_filtered = bool(sel_cust_seg or sel_cust_age)
        filter_label = f"  *(filtered: {len(df_cust_f):,} of {len(df_customers):,})*" if is_filtered else ""

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Customers" + ("¹" if is_filtered else ""), f"{len(df_cust_f):,}")
        k2.metric("VIP" + ("¹" if is_filtered else ""), f"{seg_counts_f.get('VIP', 0):,}")
        k3.metric("Avg Order Value" + ("¹" if is_filtered else ""),
                  f"${df_cust_f['avg_order_value'].mean():,.0f}")
        k4.metric("Avg Monthly Spend" + ("¹" if is_filtered else ""),
                  f"${df_cust_f['avg_monthly_spend'].mean():,.0f}")
        if is_filtered:
            st.caption(f"¹ Showing {len(df_cust_f):,} of {len(df_customers):,} customers based on active filters.")

        st.divider()

        # Charts — always unfiltered
        c1, c2 = st.columns(2)
        with c1:
            seg_counts_all = df_customers["customer_segment"].value_counts()
            plotly_pie(seg_counts_all, "Customer Segment Distribution", SEGMENT_COLORS)
        with c2:
            age_counts = df_customers["age_group"].value_counts().reindex(AGE_ORDER).dropna()
            plotly_bar(age_counts, "Customers by Age Group", color_single="#3b82f6")

        c3, c4 = st.columns(2)
        with c3:
            avg_spend_seg = (
                df_customers.groupby("customer_segment")["avg_monthly_spend"]
                .mean()
                .reindex(["VIP", "REGULAR", "NEW"])
                .dropna()
            )
            plotly_bar(avg_spend_seg, "Avg Monthly Spend by Segment", SEGMENT_COLORS)
        with c4:
            avg_aov_age = (
                df_customers.groupby("age_group")["avg_order_value"]
                .mean()
                .reindex(AGE_ORDER)
                .dropna()
            )
            plotly_bar(avg_aov_age, "Avg Order Value by Age Group", color_single="#6366f1")

        st.divider()
        st.markdown('<p class="section-label">Full Data' +
                    (" — filtered" if is_filtered else "") + "</p>", unsafe_allow_html=True)
        st.dataframe(df_cust_f, use_container_width=True, hide_index=True)
    else:
        st.warning("Customer data not found in `data/`. Run `extract_to_local.py` to generate parquet files.")

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — PRODUCT
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Product Report")
    st.markdown("""
    Product-level performance metrics including segment classification, recency, average order revenue
    and monthly revenue — mirroring the `gold.product_reports` analytical view.
    """)
    st.code("SELECT * FROM gold.product_reports;", language="sql")

    if df_products is not None:
        is_filtered_p = bool(sel_prod_cat or sel_prod_subcat or sel_prod_seg)
        prod_seg_f = df_prod_f["product_segment"].value_counts()

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Products" + ("¹" if is_filtered_p else ""), f"{len(df_prod_f):,}")
        k2.metric("Categories" + ("¹" if is_filtered_p else ""),
                  f"{df_prod_f['category'].nunique():,}")
        k3.metric("High-Performers" + ("¹" if is_filtered_p else ""),
                  f"{prod_seg_f.get('High-Performer', 0):,}")
        k4.metric("Total Revenue" + ("¹" if is_filtered_p else ""),
                  f"${df_prod_f['total_sales'].sum():,.0f}")
        if is_filtered_p:
            st.caption(f"¹ Showing {len(df_prod_f):,} of {len(df_products):,} products based on active filters.")

        st.divider()

        # Charts — always unfiltered
        c1, c2 = st.columns(2)
        with c1:
            cat_sales = (
                df_products.groupby("category")["total_sales"]
                .sum()
                .sort_values(ascending=False)
            )
            plotly_bar(cat_sales, "Total Sales by Category", color_single="#3b82f6")
        with c2:
            prod_seg_all = df_products["product_segment"].value_counts()
            plotly_pie(prod_seg_all, "Product Segment Distribution", SEGMENT_COLORS)

        c3, c4 = st.columns(2)
        with c3:
            subcat_sales = (
                df_products.groupby("subcategory")["total_sales"]
                .sum()
                .sort_values(ascending=False)
                .head(5)
                .sort_values(ascending=True)
            )
            plotly_bar(subcat_sales, "Top 5 Subcategories by Sales",
                       color_map={k: c for k, c in zip(
                           subcat_sales.index,
                           ["#f59e0b", "#3b82f6", "#10b981", "#6366f1", "#ef4444"],
                       )},
                       horizontal=True)
        with c4:
            avg_rev_cat = (
                df_products.groupby("category")["avg_monthly_revenue"]
                .mean()
                .sort_values(ascending=False)
            )
            plotly_bar(avg_rev_cat, "Avg Monthly Revenue by Category", color_single="#10b981")

        st.divider()
        subcat_share = (
            df_products.groupby(["category", "subcategory"])["total_sales"]
            .sum()
            .reset_index()
            .sort_values("total_sales", ascending=False)
        )
        subcat_share["pct"] = (
            subcat_share["total_sales"] / subcat_share["total_sales"].sum() * 100
        ).round(1)

        fig_sub = px.bar(
            subcat_share, x="subcategory", y="total_sales", color="category",
            title="Sales by Subcategory — Part-to-Whole (colour = category)",
            text=subcat_share["pct"].astype(str) + "%",
        )
        fig_sub.update_layout(
            **PLOTLY_LAYOUT,
            title=dict(text="Sales by Subcategory — Part-to-Whole (colour = category)",
                       font=dict(size=16, color="#c5cad8")),
            xaxis_tickangle=-35,
        )
        fig_sub.update_traces(textposition="outside", textfont=dict(size=10))
        st.plotly_chart(fig_sub, use_container_width=True)

        st.divider()
        st.markdown('<p class="section-label">Full Data' +
                    (" — filtered" if is_filtered_p else "") + "</p>", unsafe_allow_html=True)
        st.dataframe(df_prod_f, use_container_width=True, hide_index=True)
    else:
        st.warning("Product data not found in `data/`. Run `extract_to_local.py` to generate parquet files.")
