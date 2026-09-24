import io
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parent
DEFAULT_FILE = ROOT / "data" / "processed" / "online_retail_clean.csv.gz"

st.set_page_config(
    page_title="Sales & Revenue Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    [data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.18);
        padding: 14px 16px;
        border-radius: 12px;
    }

    [data-testid="stMetricLabel"] {
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATA LOADING AND CLEANING
# ============================================================

@st.cache_data
def clean_data_from_bytes(file_bytes, filename):

    if filename.lower().endswith((".xlsx", ".xls")):
        df = pd.read_excel(io.BytesIO(file_bytes))
    else:
        df = pd.read_csv(
            io.BytesIO(file_bytes),
            encoding_errors="ignore"
        )

    df.columns = [str(c).strip() for c in df.columns]

    required = [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "CustomerID",
        "Country",
    ]

    missing = [c for c in required if c not in df.columns]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    df["InvoiceNo"] = (
        df["InvoiceNo"]
        .astype(str)
        .str.strip()
    )

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"],
        errors="coerce"
    )

    df["Quantity"] = pd.to_numeric(
        df["Quantity"],
        errors="coerce"
    )

    df["UnitPrice"] = pd.to_numeric(
        df["UnitPrice"],
        errors="coerce"
    )

    df["Description"] = (
        df["Description"]
        .fillna("Unknown Product")
        .astype(str)
        .str.strip()
    )

    df["Country"] = (
        df["Country"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    # Identify cancelled invoices
    df["IsCancellation"] = (
        df["InvoiceNo"]
        .str.upper()
        .str.startswith("C")
    )

    # Keep only valid positive sales
    df = df[
        (~df["IsCancellation"])
        & df["InvoiceDate"].notna()
        & (df["Quantity"] > 0)
        & (df["UnitPrice"] > 0)
    ].copy()

    # Revenue calculation
    df["Revenue"] = (
        df["Quantity"] *
        df["UnitPrice"]
    )

    # Monthly period
    df["YearMonth"] = (
        df["InvoiceDate"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    # Customer ID
    df["CustomerID"] = df["CustomerID"].astype("Int64")

    return df


@st.cache_data
def load_default():

    if not DEFAULT_FILE.exists():
        return None

    df = pd.read_csv(
        DEFAULT_FILE,
        parse_dates=[
            "InvoiceDate",
            "YearMonth"
        ]
    )

    if "CustomerID" in df.columns:
        df["CustomerID"] = (
            df["CustomerID"]
            .astype("Int64")
        )

    return df


# ============================================================
# FORMATTING FUNCTIONS
# ============================================================

def money(value):

    value = float(value)

    if abs(value) >= 1_000_000:
        return f"£{value / 1_000_000:.2f}M"

    if abs(value) >= 1_000:
        return f"£{value / 1_000:.1f}K"

    return f"£{value:,.2f}"


def integer(value):

    return f"{int(round(float(value))):,}"


def compact_number(value):

    value = float(value)

    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"

    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"

    return f"{value:,.0f}"


# ============================================================
# HEADER
# ============================================================

st.title(
    "📊 Sales & Revenue Analysis Dashboard"
)

st.caption(
    "UCI Online Retail dataset • "
    "Interactive sales, revenue, product and geographic analysis"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("📁 Data")

    uploaded = st.file_uploader(
        "Upload Online Retail CSV / Excel",
        type=[
            "csv",
            "xlsx",
            "xls"
        ],
        help=(
            "Supported formats: CSV, XLSX and XLS."
        ),
    )

    if uploaded is not None:

        try:

            df = clean_data_from_bytes(
                uploaded.getvalue(),
                uploaded.name
            )

            st.success(
                f"Loaded: {uploaded.name}"
            )

        except Exception as e:

            st.error(str(e))
            st.stop()

    else:

        df = load_default()

    if df is None:

        st.warning(
            "No local dataset found. "
            "Run the data preparation script "
            "or upload the UCI Online Retail file here."
        )

        st.info(
            "Source: UCI Machine Learning Repository — Online Retail"
        )

        st.stop()

    st.divider()

    st.header("🔎 Filters")

    min_date = (
        df["InvoiceDate"]
        .min()
        .date()
    )

    max_date = (
        df["InvoiceDate"]
        .max()
        .date()
    )

    date_range = st.date_input(
        "Date range",
        value=(
            min_date,
            max_date
        ),
        min_value=min_date,
        max_value=max_date,
    )

    countries = st.multiselect(
        "Country",
        sorted(
            df["Country"]
            .dropna()
            .unique()
        ),
        default=[],
    )

    product_search = st.text_input(
        "Product contains",
        placeholder="e.g. POSTAGE, HEART...",
    )

    st.divider()

    st.caption(
        f"Available data: "
        f"{min_date} → {max_date}"
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered = df.copy()


# Date filter
if (
    isinstance(date_range, (tuple, list))
    and len(date_range) == 2
):

    start = pd.to_datetime(
        date_range[0]
    )

    end = (
        pd.to_datetime(date_range[1])
        + pd.Timedelta(days=1)
    )

    filtered = filtered[
        (filtered["InvoiceDate"] >= start)
        &
        (filtered["InvoiceDate"] < end)
    ]

elif hasattr(date_range, "year"):

    selected = pd.to_datetime(
        date_range
    )

    filtered = filtered[
        filtered["InvoiceDate"].dt.date
        == selected.date()
    ]


# Country filter
if countries:

    filtered = filtered[
        filtered["Country"].isin(countries)
    ]


# Product search
if product_search:

    filtered = filtered[
        filtered["Description"].str.contains(
            product_search,
            case=False,
            na=False
        )
    ]


# ============================================================
# KPI CALCULATIONS
# ============================================================

revenue = filtered["Revenue"].sum()

quantity = filtered["Quantity"].sum()

orders = filtered["InvoiceNo"].nunique()

customers = (
    filtered["CustomerID"]
    .dropna()
    .nunique()
)

aov = (
    revenue / orders
    if orders
    else 0
)


# ============================================================
# KPI CARDS
# ============================================================

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric(
    "Total Revenue",
    money(revenue)
)

k2.metric(
    "Total Orders",
    integer(orders)
)

k3.metric(
    "Total Quantity",
    compact_number(quantity)
)

k4.metric(
    "Average Order Value",
    money(aov)
)

k5.metric(
    "Unique Customers",
    integer(customers)
)


st.caption(
    f"Showing {len(filtered):,} valid transaction rows "
    f"after applying the selected filters."
)

st.divider()


# ============================================================
# EMPTY DATA CHECK
# ============================================================

if filtered.empty:

    st.warning(
        "No transactions match the selected filters."
    )

    st.stop()


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.subheader(
    "💡 Key Business Insights"
)


# Highest revenue month
insight_month = (
    filtered
    .groupby(
        "YearMonth",
        as_index=False
    )["Revenue"]
    .sum()
    .sort_values(
        "Revenue",
        ascending=False
    )
)


# Highest revenue product
insight_product = (
    filtered
    .groupby(
        "Description",
        as_index=False
    )["Revenue"]
    .sum()
    .sort_values(
        "Revenue",
        ascending=False
    )
)


# Highest revenue country
insight_country = (
    filtered
    .groupby(
        "Country",
        as_index=False
    )["Revenue"]
    .sum()
    .sort_values(
        "Revenue",
        ascending=False
    )
)


best_month = insight_month.iloc[0]

best_product = insight_product.iloc[0]

best_country = insight_country.iloc[0]


revenue_per_customer = (
    revenue / customers
    if customers
    else 0
)


i1, i2, i3, i4 = st.columns(4)


i1.metric(
    "Highest Revenue Month",
    best_month[
        "YearMonth"
    ].strftime("%b %Y"),
    f"£{best_month['Revenue']:,.2f}",
)


i2.metric(
    "Top Revenue Product",
    str(
        best_product["Description"]
    )[:24],
    f"£{best_product['Revenue']:,.2f}",
)


i3.metric(
    "Top Revenue Country",
    str(
        best_country["Country"]
    ),
    f"£{best_country['Revenue']:,.2f}",
)


i4.metric(
    "Revenue per Customer",
    money(
        revenue_per_customer
    ),
)


st.divider()


# ============================================================
# MONTHLY AGGREGATIONS
# ============================================================

monthly = (
    filtered
    .groupby(
        "YearMonth",
        as_index=False
    )
    .agg(
        Revenue=("Revenue", "sum"),
        Orders=("InvoiceNo", "nunique"),
        Quantity=("Quantity", "sum"),
    )
    .sort_values("YearMonth")
)


# ============================================================
# PRODUCT AGGREGATIONS
# ============================================================

top_products = (
    filtered
    .groupby(
        "Description",
        as_index=False
    )
    .agg(
        Revenue=("Revenue", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("InvoiceNo", "nunique"),
    )
    .sort_values(
        "Revenue",
        ascending=False
    )
    .head(10)
)


# ============================================================
# COUNTRY AGGREGATIONS
# ============================================================

country = (
    filtered
    .groupby(
        "Country",
        as_index=False
    )
    .agg(
        Revenue=("Revenue", "sum"),
        Orders=("InvoiceNo", "nunique"),
        Quantity=("Quantity", "sum"),
    )
    .sort_values(
        "Revenue",
        ascending=False
    )
)


top_countries = (
    country
    .head(15)
    .copy()
)


# ============================================================
# REVENUE & ORDER TREND
# ============================================================

st.subheader(
    "📈 Revenue & Order Trend"
)


trend_left, trend_right = st.columns(
    [2.1, 1]
)


# Revenue trend
with trend_left:

    fig = px.line(
        monthly,
        x="YearMonth",
        y="Revenue",
        markers=True,
        labels={
            "YearMonth": "Month",
            "Revenue": "Revenue (£)"
        },
        hover_data={
            "Revenue": ":,.2f",
            "YearMonth": "|%b %Y"
        },
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{x|%b %Y}</b>"
            "<br>Revenue: £%{y:,.2f}"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        ),
        xaxis_title="",
        yaxis_title="Revenue (£)",
    )

    fig.update_yaxes(
        tickprefix="£",
        separatethousands=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# Order trend
with trend_right:

    fig = px.bar(
        monthly,
        x="YearMonth",
        y="Orders",
        labels={
            "YearMonth": "Month",
            "Orders": "Orders"
        },
        hover_data={
            "Orders": ":,",
            "YearMonth": "|%b %Y"
        },
    )

    fig.update_layout(
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        ),
        xaxis_title="",
        yaxis_title="Orders",
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PRODUCT PERFORMANCE
# ============================================================

st.subheader(
    "🏆 Product Performance"
)


product_left, product_right = st.columns(2)


# Top products by revenue
with product_left:

    fig = px.bar(
        top_products.sort_values(
            "Revenue"
        ),
        x="Revenue",
        y="Description",
        orientation="h",
        labels={
            "Revenue": "Revenue (£)",
            "Description": ""
        },
        hover_data={
            "Revenue": ":,.2f",
            "Quantity": ":,",
            "Orders": ":,"
        },
    )

    fig.update_layout(
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        ),
        xaxis_title="Revenue (£)",
        yaxis_title="",
    )

    fig.update_xaxes(
        tickprefix="£",
        separatethousands=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# Top products by quantity
with product_right:

    fig = px.bar(
        top_products.sort_values(
            "Quantity"
        ),
        x="Quantity",
        y="Description",
        orientation="h",
        labels={
            "Quantity": "Units Sold",
            "Description": ""
        },
        hover_data={
            "Quantity": ":,",
            "Revenue": ":,.2f",
            "Orders": ":,"
        },
    )

    fig.update_layout(
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        ),
        xaxis_title="Units Sold",
        yaxis_title="",
    )

    fig.update_xaxes(
        separatethousands=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# GEOGRAPHIC ANALYSIS
# ============================================================

st.subheader(
    "🌍 Geographic Revenue Analysis"
)


geo_left, geo_right = st.columns(
    [1.6, 1]
)


# Revenue by country
with geo_left:

    fig = px.bar(
        top_countries.sort_values(
            "Revenue"
        ),
        x="Revenue",
        y="Country",
        orientation="h",
        labels={
            "Revenue": "Revenue (£)",
            "Country": ""
        },
        hover_data={
            "Revenue": ":,.2f",
            "Orders": ":,",
            "Quantity": ":,"
        },
    )

    fig.update_layout(
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        ),
        xaxis_title="Revenue (£)",
        yaxis_title="",
    )

    fig.update_xaxes(
        tickprefix="£",
        separatethousands=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# Revenue share
with geo_right:

    share = (
        top_countries
        .head(10)
        .copy()
    )

    fig = px.pie(
        share,
        names="Country",
        values="Revenue",
        hole=0.48,
        labels={
            "Revenue": "Revenue (£)"
        },
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate=(
            "%{label}"
            "<br>Revenue: £%{value:,.2f}"
            "<br>Share: %{percent}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        ),
        legend_title_text="Country",
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# COUNTRY SUMMARY TABLE
# ============================================================

st.subheader(
    "📋 Top Countries Summary"
)


country_table = (
    country
    .head(15)
    .copy()
)


country_table["Revenue"] = (
    country_table["Revenue"]
    .map(
        lambda x:
        f"£{x:,.2f}"
    )
)


country_table["Orders"] = (
    country_table["Orders"]
    .map(
        lambda x:
        f"{int(x):,}"
    )
)


country_table["Quantity"] = (
    country_table["Quantity"]
    .map(
        lambda x:
        f"{int(x):,}"
    )
)


st.dataframe(
    country_table,
    use_container_width=True,
    hide_index=True,
)


# ============================================================
# FILTERED TRANSACTION DATA
# ============================================================

with st.expander(
    "🔍 View Filtered Transaction Data"
):

    display_cols = [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "Revenue",
        "CustomerID",
        "Country",
    ]

    st.dataframe(
        filtered[
            display_cols
        ]
        .sort_values(
            "InvoiceDate",
            ascending=False
        )
        .head(1000),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# DOWNLOAD FILTERED DATA
# ============================================================

csv = (
    filtered
    .to_csv(index=False)
    .encode("utf-8")
)


st.download_button(
    "⬇️ Download Filtered Data",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv",
)


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "Source: UCI Machine Learning Repository, Online Retail. "
    "Revenue = Quantity × UnitPrice. "
    "The dashboard excludes cancelled and invalid sales "
    "from the main sales analysis."
)