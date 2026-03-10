import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Enterprise Risk Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------- Load data ----------
@st.cache_data
def load_data():
    df = pd.read_csv("data/synthetic_risk_register.csv")

    numeric_cols = ["impact_level", "probability_level", "priority_level"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "owner" not in df.columns:
        default_owners = [
            "IT", "Finance", "Operations", "Strategy", "Facilities",
            "HR", "Safety", "Compliance", "Security", "Communications"
        ]
        df["owner"] = (default_owners * ((len(df) // len(default_owners)) + 1))[:len(df)]

    df["risk_score"] = df["impact_level"] * df["probability_level"]

    def classify_risk(score):
        if score >= 15:
            return "High"
        elif score >= 8:
            return "Medium"
        return "Low"

    df["risk_level"] = df["risk_score"].apply(classify_risk)
    return df

df = load_data()

# ---------- Sidebar ----------
st.sidebar.title("Enterprise Risk")
st.sidebar.caption("Interactive monitoring dashboard")

selected_categories = st.sidebar.multiselect(
    "Risk Category",
    options=sorted(df["risk_category"].dropna().unique()),
    default=sorted(df["risk_category"].dropna().unique())
)

selected_levels = st.sidebar.multiselect(
    "Risk Level",
    options=["High", "Medium", "Low"],
    default=["High", "Medium", "Low"]
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
].copy()

# ---------- Header ----------
st.title("Enterprise Risk Dashboard")
st.markdown("Executive overview of synthetic enterprise risk exposure and prioritization.")

# ---------- KPIs ----------
total_risks = len(filtered_df)
high_risks = len(filtered_df[filtered_df["risk_level"] == "High"])
medium_risks = len(filtered_df[filtered_df["risk_level"] == "Medium"])
avg_score = round(filtered_df["risk_score"].mean(), 1) if total_risks > 0 else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Risks", total_risks)
c2.metric("High Risks", high_risks)
c3.metric("Medium Risks", medium_risks)
c4.metric("Avg Risk Score", avg_score)

st.markdown("---")

# ---------- Row 1 ----------
left, right = st.columns([1, 1])

with left:
    st.subheader("Risk Distribution by Category")
    if not filtered_df.empty:
        category_counts = (
            filtered_df.groupby("risk_category")["risk_id"]
            .count()
            .reset_index(name="risk_count")
            .sort_values("risk_count", ascending=False)
        )

        fig_bar = px.bar(
            category_counts,
            x="risk_category",
            y="risk_count",
            text="risk_count"
        )
        fig_bar.update_layout(
            xaxis_title="Category",
            yaxis_title="Number of Risks",
            showlegend=False,
            height=420
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("No category data available.")

with right:
    st.subheader("Risk Level Mix")
    if not filtered_df.empty:
        risk_mix = filtered_df["risk_level"].value_counts().reset_index()
        risk_mix.columns = ["risk_level", "count"]

        fig_pie = px.pie(
            risk_mix,
            names="risk_level",
            values="count",
            hole=0.55
        )
        fig_pie.update_layout(height=420)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("No risk level data available.")

# ---------- Row 2 ----------
left2, right2 = st.columns([1.2, 1])

with left2:
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

    fig_matrix = go.Figure(
        data=go.Heatmap(
            z=z_values,
            text=text_values,
            texttemplate="%{text}",
            textfont={"size": 18},
            x=[1, 2, 3, 4, 5],
            y=[5, 4, 3, 2, 1],
            colorscale=[
                [0.0, "#2e7d32"],
                [0.33, "#2e7d32"],
                [0.34, "#f9a825"],
                [0.66, "#f9a825"],
                [0.67, "#c62828"],
                [1.0, "#c62828"],
            ],
            zmin=0,
            zmax=2,
            showscale=False,
            hovertemplate="Impact: %{x}<br>Probability: %{y}<br>Risks: %{text}<extra></extra>"
        )
    )

    fig_matrix.update_layout(
        xaxis_title="Impact",
        yaxis_title="Probability",
        height=520
    )

    st.plotly_chart(fig_matrix, use_container_width=True)

with right2:
    st.subheader("Top Risks")
    if not filtered_df.empty:
        top_risks = (
            filtered_df.sort_values(
                ["risk_score", "impact_level", "probability_level"],
                ascending=[False, False, False]
            )[
                [
                    "risk_id",
                    "risk_category",
                    "owner",
                    "risk_score",
                    "risk_level"
                ]
            ]
            .head(7)
        )
        st.dataframe(top_risks, use_container_width=True, hide_index=True)
    else:
        st.warning("No top risks available.")

# ---------- Row 3 ----------
st.subheader("Risk Score by Owner")
if not filtered_df.empty:
    owner_scores = (
        filtered_df.groupby("owner", as_index=False)["risk_score"]
        .mean()
        .sort_values("risk_score", ascending=False)
    )

    fig_owner = px.bar(
        owner_scores,
        x="owner",
        y="risk_score",
        text="risk_score"
    )
    fig_owner.update_layout(
        xaxis_title="Owner",
        yaxis_title="Average Risk Score",
        height=420
    )
    st.plotly_chart(fig_owner, use_container_width=True)
else:
    st.warning("No owner score data available.")

# ---------- Detailed table ----------
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

if not filtered_df.empty:
    st.dataframe(
        filtered_df[existing_cols].sort_values("risk_score", ascending=False),
        use_container_width=True,
        hide_index=True
    )
else:
    st.warning("No detailed risks available for the selected filters.")

# ---------- Download ----------
st.subheader("Export")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download filtered data as CSV",
    data=csv,
    file_name="filtered_risk_data.csv",
    mime="text/csv"
)
