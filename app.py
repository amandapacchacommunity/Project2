import pandas as pd
import streamlit as st
import plotly.graph_objects as go

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

# Add owner if missing
if "owner" not in df.columns:
    default_owners = [
        "IT", "Finance", "Operations", "Strategy", "Facilities",
        "HR", "Safety", "Compliance", "Security", "Communications"
    ]
    df["owner"] = (default_owners * ((len(df) // len(default_owners)) + 1))[:len(df)]

# Risk score and level
df["risk_score"] = df["impact_level"] * df["probability_level"]

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

# Executive summary
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

# True 5x5 risk matrix
st.subheader("5x5 Enterprise Risk Matrix")

matrix_df = pd.DataFrame(
    [(p, i) for p in range(1, 6) for i in range(1, 6)],
    columns=["probability_level", "impact_level"]
)

counts = (
    filtered_df.groupby(["probability_level", "impact_level"])
    .size()
    .reset_index(name="count")
)

matrix_df = matrix_df.merge(
    counts,
    on=["probability_level", "impact_level"],
    how="left"
).fillna({"count": 0})

def zone_color(prob, impact):
    score = prob * impact
    if score >= 15:
        return "High"
    elif score >= 8:
        return "Medium"
    return "Low"

matrix_df["zone"] = matrix_df.apply(
    lambda row: zone_color(row["probability_level"], row["impact_level"]),
    axis=1
)

color_map = {"Low": 0, "Medium": 1, "High": 2}
matrix_df["zone_code"] = matrix_df["zone"].map(color_map)

z_values = []
text_values = []

for prob in range(5, 0, -1):
    row_colors = []
    row_text = []
    for impact in range(1, 6):
        match = matrix_df[
            (matrix_df["probability_level"] == prob) &
            (matrix_df["impact_level"] == impact)
        ].iloc[0]
        row_colors.append(match["zone_code"])
        row_text.append(str(int(match["count"])))
    z_values.append(row_colors)
    text_values.append(row_text)

fig = go.Figure(
    data=go.Heatmap(
        z=z_values,
        text=text_values,
        texttemplate="%{text}",
        textfont={"size": 18},
        x=[1, 2, 3, 4, 5],
        y=[5, 4, 3, 2, 1],
        colorscale=[
            [0.0, "#3cb371"],
            [0.33, "#3cb371"],
            [0.34, "#f4d03f"],
            [0.66, "#f4d03f"],
            [0.67, "#e74c3c"],
            [1.0, "#e74c3c"],
        ],
        zmin=0,
        zmax=2,
        showscale=False,
        hovertemplate="Impact: %{x}<br>Probability: %{y}<br>Risks: %{text}<extra></extra>"
    )
)

fig.update_layout(
    xaxis_title="Impact",
    yaxis_title="Probability",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

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
        return "background-color: #e74c3c; color: white"
    elif val == "Medium":
        return "background-color: #f4d03f; color: black"
    elif val == "Low":
        return "background-color: #3cb371; color: white"
    return ""

if not filtered_df.empty:
    styled_df = filtered_df[existing_cols].style.map(
        highlight_risk, subset=["risk_level"]
    )
    st.dataframe(styled_df, use_container_width=True)
else:
    st.warning("No detailed risks available.")

# Download button
st.subheader("Download Filtered Data")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download filtered risk data as CSV",
    data=csv,
    file_name="filtered_risk_data.csv",
    mime="text/csv"
)
