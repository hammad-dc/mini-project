import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Q-Comm Pulse",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS Theme ──────────────────────────────────────────────────────────
st.markdown("""
    <style>
        .stApp { background-color: #0f1117; color: #e0e0e0; }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1d2e 0%, #16213e 100%);
            border-right: 1px solid #2d3561;
        }

        [data-testid="stMetric"] {
            background: linear-gradient(135deg, #1e2235 0%, #252a40 100%);
            border: 1px solid #2d3561;
            border-radius: 12px;
            padding: 16px 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        [data-testid="stMetricValue"] { color: #7eb3ff; font-size: 2rem !important; }
        [data-testid="stMetricLabel"] { color: #9ca3af; font-size: 0.85rem !important; }
        [data-testid="stMetricDelta"] { font-size: 0.8rem !important; }

        .stTabs [data-baseweb="tab-list"] {
            background: #1a1d2e;
            border-radius: 10px;
            padding: 4px;
            gap: 4px;
        }
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 8px;
            color: #9ca3af;
            font-weight: 500;
            padding: 8px 20px;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #2d3561, #3d4a7a) !important;
            color: #7eb3ff !important;
        }

        .dashboard-header {
            background: linear-gradient(135deg, #1e2235 0%, #2d3561 100%);
            border-radius: 16px;
            padding: 24px 32px;
            margin-bottom: 24px;
            border: 1px solid #3d4a7a;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        }

        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #6b7280;
            background: #1a1d2e;
            border-radius: 12px;
            border: 1px dashed #2d3561;
        }

        hr { border-color: #2d3561 !important; }
    </style>
""", unsafe_allow_html=True)

# ── Data Loading ──────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Blinkit_Master_Data.csv")

@st.cache_data(show_spinner="Loading data...")
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    date_cols = [c for c in df.columns if "date" in c or "time" in c]
    for col in date_cols:
        try:
            df[col] = pd.to_datetime(df[col], errors="coerce")
        except Exception:
            pass

    num_candidates = [
        "order_value", "revenue", "total_price", "price",
        "delivery_time_minutes", "delay_minutes", "actual_delivery_time",
        "estimated_delivery_time", "quantity", "damaged_units",
        "rating", "customer_rating",
    ]
    for col in num_candidates:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def find_col(df: pd.DataFrame, candidates: list) -> str:
    for c in candidates:
        if c in df.columns:
            return c
    return None


try:
    df_raw = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(f"Data file not found at `{DATA_PATH}`. Place **Blinkit_Master_Data.csv** next to app.py.")
    st.stop()

# ── Column Mapping ────────────────────────────────────────────────────────────
COL = {
    "area"    : find_col(df_raw, ["area", "location", "city", "zone", "region", "delivery_area"]),
    "category": find_col(df_raw, ["category", "product_category", "item_category"]),
    "date"    : find_col(df_raw, ["order_date", "date", "delivery_date", "order_time"]),
    "revenue" : find_col(df_raw, ["revenue", "order_value", "total_price", "price"]),
    "orders"  : find_col(df_raw, ["order_id", "id"]),
    "delay"   : find_col(df_raw, ["delay_minutes", "actual_delivery_time", "delivery_time_minutes"]),
    "damaged" : find_col(df_raw, ["damaged_units", "damaged_stock", "damaged"]),
    "rating"  : find_col(df_raw, ["rating", "customer_rating", "review_score"]),
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ Q-Comm Pulse")
    st.markdown("*Real-time Operations Dashboard*")
    st.divider()
    st.markdown("### 🔍 Filters")

    # Area filter
    if COL["area"]:
        all_areas = sorted(df_raw[COL["area"]].dropna().unique().tolist())
        selected_areas = st.multiselect("📍 Area", options=all_areas, default=all_areas)
    else:
        selected_areas = []
        st.info("No area column detected.")

    # Category filter
    if COL["category"]:
        all_cats = sorted(df_raw[COL["category"]].dropna().unique().tolist())
        selected_cats = st.multiselect("🏷️ Category", options=all_cats, default=all_cats)
    else:
        selected_cats = []
        st.info("No category column detected.")

    # Date range filter
    st.markdown("#### 📅 Date Range")
    if COL["date"] and df_raw[COL["date"]].notna().any():
        min_date = df_raw[COL["date"]].min().date()
        max_date = df_raw[COL["date"]].max().date()
        date_range = st.date_input("Select range", value=(min_date, max_date),
                                   min_value=min_date, max_value=max_date)
    else:
        date_range = None
        st.info("No date column detected.")

    st.divider()
    st.caption("Data Source: Blinkit Master Dataset")

# ── Apply Filters ─────────────────────────────────────────────────────────────
df = df_raw.copy()

if COL["area"] and selected_areas:
    df = df[df[COL["area"]].isin(selected_areas)]

if COL["category"] and selected_cats:
    df = df[df[COL["category"]].isin(selected_cats)]

if date_range and COL["date"] and len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    df = df[df[COL["date"]].between(start, end)]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
    <div class="dashboard-header">
        <h1 style="margin:0; color:#7eb3ff; font-size:2rem; font-weight:700;">
            ⚡ Q-Comm Pulse
        </h1>
        <p style="margin:4px 0 0; color:#9ca3af; font-size:0.95rem;">
            Quick Commerce Operations Intelligence Platform
        </p>
    </div>
""", unsafe_allow_html=True)

# ── Empty state helper ─────────────────────────────────────────────────────────
def empty_state(msg="No data matches the selected filters."):
    st.markdown(f"""
        <div class="empty-state">
            <h3>📭 No Data Available</h3>
            <p>{msg}</p>
        </div>
    """, unsafe_allow_html=True)


if df.empty:
    empty_state("Try adjusting your sidebar filters to see data.")
    st.stop()

# ── Plotly shared layout ───────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="#1a1d2e",
    plot_bgcolor="#1a1d2e",
    font=dict(color="#e0e0e0", family="Inter, sans-serif"),
    xaxis=dict(gridcolor="#2d3561", linecolor="#2d3561", tickcolor="#9ca3af"),
    yaxis=dict(gridcolor="#2d3561", linecolor="#2d3561", tickcolor="#9ca3af"),
    margin=dict(l=40, r=20, t=50, b=40),
    legend=dict(bgcolor="#252a40", bordercolor="#2d3561", borderwidth=1),
)
COLOR_SEQ = px.colors.qualitative.Set2

st.markdown("<br>", unsafe_allow_html=True)
## ── Management Summary / Critical Alerts ──
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🛑 Critical Alerts", unsafe_allow_html=True)
alerts = []
if COL["delay"] and COL["area"]:
    week_ago = df[COL["date"]].max() - pd.Timedelta(days=7) if COL["date"] else None
    if week_ago is not None:
        recent = df[df[COL["date"]] >= week_ago]
        area_delay = recent.groupby(COL["area"])[COL["delay"]].mean().sort_values(ascending=False)
        if not area_delay.empty:
            top_area = area_delay.idxmax()
            alerts.append(f"⚠️ Area '{top_area}' has seen a {area_delay.max():.1f} min avg delay this week.")
if COL["damaged"] and COL["category"]:
    cat_dmg = df.groupby(COL["category"])[COL["damaged"]].sum().sort_values(ascending=False)
    if not cat_dmg.empty:
        top_cat = cat_dmg.idxmax()
        alerts.append(f"⚠️ Category '{top_cat}' has the highest damage incidents.")
if alerts:
    for alert in alerts:
        st.warning(alert)
else:
    st.info("No critical alerts at this time.")

# ── KPI Cards ─────────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
with c1:
    if COL["revenue"]:
        total_rev = df[COL["revenue"]].sum()
        st.metric("💰 Total Revenue", f"₹{total_rev:,.0f}", f"{len(df):,} transactions")
    else:
        st.metric("💰 Total Revenue", "N/A")
with c2:
    if COL["delay"]:
        avg_delay = df[COL["delay"]].mean()
        st.metric("⏱️ Avg Delivery Delay",
                  f"{avg_delay:.1f} min" if pd.notna(avg_delay) else "N/A",
                  "minutes per order")
    else:
        st.metric("⏱️ Avg Delivery Delay", "N/A")
with c3:
    if COL["orders"]:
        total_orders = df[COL["orders"]].nunique()
        st.metric("📦 Total Orders", f"{total_orders:,}", "unique orders")
    else:
        st.metric("📦 Total Orders", f"{len(df):,}", "records")
st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_log, tab_inv, tab_cust = st.tabs(["🚚  Logistics", "📦  Inventory", "⭐  Customer"])

## ─── LOGISTICS ── Delay Heatmap ──
with tab_log:
    st.subheader("🚚 Top 10 Trouble Zones (Impact Score)")
    if not COL["area"] or not COL["delay"]:
        empty_state("Area or delay column not found in dataset.")
    else:
        area_stats = df.groupby(COL["area"]).agg(
            avg_delay=(COL["delay"], "mean"),
            order_volume=(COL["area"], "count")
        )
        area_stats["impact_score"] = area_stats["avg_delay"] * area_stats["order_volume"]
        top_areas = area_stats.sort_values("impact_score", ascending=False).head(10).reset_index()
        if top_areas.empty:
            empty_state("No delivery data for the selected filters.")
        else:
            fig = px.bar(
                top_areas, x=COL["area"], y="impact_score",
                color="impact_score",
                text=top_areas["avg_delay"].round(1).astype(str) + " min avg",
                title="Top 10 Areas by Impact Score",
                labels={COL["area"]: "Area", "impact_score": "Impact Score"}
            )
            fig.update_traces(textposition="outside", textfont_size=11)
            fig.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False,
                              title_font_size=16, title_font_color="#7eb3ff")
            st.plotly_chart(fig, width="stretch")
            with st.expander("📊 Raw Data"):
                st.dataframe(top_areas, width="stretch")

## ─── INVENTORY ── Wastage vs Revenue ──
with tab_inv:
    st.subheader("📦 Damage Percentage per Category")
    if not COL["category"] or not COL["damaged"]:
        empty_state("Category or damaged stock column not found in dataset.")
    else:
        sold_col = COL["orders"] if COL["orders"] else "sold_units"
        cat_stats = df.groupby(COL["category"]).agg(
            damaged=(COL["damaged"], "sum"),
            sold=(sold_col, "count")
        )
        cat_stats["damage_pct"] = cat_stats["damaged"] / (cat_stats["damaged"] + cat_stats["sold"] + 1e-6)
        top_cats = cat_stats.sort_values("damage_pct", ascending=False).head(10).reset_index()
        if top_cats.empty:
            empty_state("No inventory data for the selected filters.")
        else:
            fig = px.bar(
                top_cats, x=COL["category"], y="damage_pct",
                color="damage_pct",
                text=(top_cats["damage_pct"]*100).round(2).astype(str) + "%",
                title="Top Categories by Damage Percentage",
                labels={COL["category"]: "Category", "damage_pct": "Damage %"}
            )
            fig.update_traces(textposition="outside", textfont_size=11)
            fig.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False,
                              title_font_size=16, title_font_color="#7eb3ff")
            st.plotly_chart(fig, width="stretch")
            with st.expander("📊 Raw Data"):
                st.dataframe(top_cats, width="stretch")

## ─── CUSTOMER ── Sentiment Driver ──
with tab_cust:
    st.subheader("⭐ Sentiment by Delay Buckets")
    if not COL["delay"] or not COL["rating"]:
        empty_state("Delay or rating column not found in dataset.")
    else:
        df_buckets = df[[COL["delay"], COL["rating"]]].dropna().copy()
        bins = [0, 5, 15, df_buckets[COL["delay"]].max()+1]
        labels = ["0-5 min", "5-15 min", "15+ min"]
        df_buckets["delay_bucket"] = pd.cut(df_buckets[COL["delay"]], bins=bins, labels=labels, right=False)
        box_data = df_buckets.dropna(subset=["delay_bucket", COL["rating"]])
        if box_data.empty:
            empty_state("No customer data for the selected filters.")
        else:
            fig = px.box(
                box_data, x="delay_bucket", y=COL["rating"],
                color="delay_bucket",
                title="Customer Ratings by Delay Bucket",
                labels={"delay_bucket": "Delay Bucket", COL["rating"]: "Rating"}
            )
            fig.update_layout(**PLOTLY_LAYOUT,
                              title_font_size=16, title_font_color="#7eb3ff")
            st.plotly_chart(fig, width="stretch")
            with st.expander("📊 Raw Data"):
                st.dataframe(box_data, width="stretch")

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='text-align:center; color:#4b5563; font-size:0.8rem;'>"
    "⚡ Q-Comm Pulse &nbsp;|&nbsp; Powered by Streamlit & Plotly &nbsp;|&nbsp; Blinkit Dataset"
    "</p>",
    unsafe_allow_html=True,
)
