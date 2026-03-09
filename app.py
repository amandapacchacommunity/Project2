import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Enterprise Risk Dashboard", layout="wide")

st.title("Enterprise Risk Dashboard")
st.caption("Synthetic risk register analytics project")

# Load data
df = pd.read_csv("data/synthetic_risk_register.csv")

# Clean numeric columns
numeric_cols = ["impact_level", "probability_level", "priority_level"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Add owner column if missing
if "owner" not in df.columns:
    default_owners = [
        "IT", "Finance", "Operations", "Strategy", "Facilities",
        "HR", "Safety", "Compliance", "Security", "Communications"
    ]
    df["owner"] = (default_owners * ((len(df) // len(default_owners)) + 1))[:len(df)]

# Create risk score
df["risk_score"] = df["impact_level"] * df["probability_level"]

# Create risk level
def classify_risk(score):
    if score >= 15:
        return "High"
    elif score >= 8:
        return "Medium"
    return "Low"

df["risk_level"] = df["risk_score"].apply(classify_risk)

# Sidebar
st.sidebar.title("Risk Analytics Dashboard")
st.sidebar.markdown("Enterprise Risk Monitoring")

selected_categories = st.sidebar.multiselect(
    "Risk Category",
    options=sorted(df["risk_category"].dropna().unique()),
    default=sorted(df["risk_category"].dropna().unique())
)

selected_levels = st.sidebar.multiselect(
    "Risk Level",
    options=sorted(df["risk_level"].dropna().unique()),
    default=sorted(df["risk_level"].dropna().unique())
)

selected_owners = st.sidebar.multiselect(
    "Owner",
    options=sorted(df["owner"].dropna().unique()),
    default=sorted(df["owner"].dropna().unique())
)

filtered_df = df[
    (df["risk_category"].isin(selected_categories)) &
    (df["risk_level"].isin(selected_levels)) &
    (df["owner"].isin(selected_owners))
]

# KPIs
total_risks = len(filtered_df)
high_risks = len(filtered_df[filtered_df["risk_level"] == "High"])
avg_impact = round(filtered_df["impact_level"].mean(), 2) if total_risks > 0 else 0
avg_probability = round(filtered_df["probability_level"].mean(), 2) if total_risks > 0 else 0

st.subheader("Executive Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Risks", total_risks)
col2.metric("High Risks", high_risks)
col3.metric("Avg Impact", avg_impact)
col4.metric("Avg Probability", avg_probability)

# Risk level distribution
st.subheader("Risk Level Distribution")
if not filtered_df.empty:
    risk_counts = filtered_df["risk_level"].value_counts()
    st.bar_chart(risk_counts)
else:
    st.warning("No data available for the selected filters.")

# Risks by category
st.subheader("Risks by Category")
category_counts = (
    filtered_df.groupby("risk_category")["risk_id"]
    .count()
    .reset_index(name="risk_count")
    .sort_values("risk_count", ascending=False)
)

if not category_counts.empty:
    st.bar_chart(category_counts.set_index("risk_category"))
else:
    st.warning("No category data available.")

# Risk heatmap
st.subheader("Risk Heatmap")

heatmap = (
    filtered_df.groupby(["probability_level", "impact_level"])
    .size()
    .reset_index(name="count")
)

if not heatmap.empty:
    fig = px.density_heatmap(
        heatmap,
        x="impact_level",
        y="probability_level",
        z="count",
        color_continuous_scale="RdYlGn_r",
        text_auto=True
    )
    fig.update_layout(
        xaxis_title="Impact Level",
        yaxis_title="Probability Level"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No heatmap data available.")

# Detailed risk register
st.subheader("Detailed Risk Register")

display_cols = [
    "risk_id",
    "risk_category",
    "risk_description",
    "owner",
    "impact_level",
    "probability_level",
    "risk_score",
    "risk_level"
]

existing_cols = [col for col in display_cols if col in filtered_df.columns]

def highlight_risk(val):
    if val == "High":
        return "background-color: #ff4b4b; color: white"
    elif val == "Medium":
        return "background-color: #ffa500; color: black"
    elif val == "Low":
        return "background-color: #3cb371; color: white"
    return ""

if not filtered_df.empty:
    styled_df = filtered_df[existing_cols].style.map(highlight_risk, subset=["risk_level"])
    st.dataframe(styled_df, use_container_width=True)
else:
    st.warning("No detailed risks available.")

# Download filtered data
st.subheader("Download Filtered Data")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download filtered risk data as CSV",
    data=csv,
    file_name="filtered_risk_data.csv",
    mime="text/csv"
)
