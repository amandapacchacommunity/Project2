from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

st.set_page_config(page_title="Synthetic ERM Dashboard", layout="wide")


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    risks = pd.read_csv(DATA_DIR / "synthetic_risk_register.csv")
    actions = pd.read_csv(DATA_DIR / "synthetic_actions.csv")
    aggs = pd.read_csv(DATA_DIR / "synthetic_aggregations.csv")
    actions["deadline"] = pd.to_datetime(actions["deadline"])
    return risks, actions, aggs


risks_df, actions_df, aggs_df = load_data()

st.title("Enterprise Risk Register Demo")
st.caption("Synthetic data only. Safe for public GitHub demos.")

left, right = st.columns(2)
with left:
    st.metric("Risk-plan records", len(risks_df))
    st.metric("Action records", len(actions_df))
with right:
    st.metric("Overdue actions", int((actions_df["status"] == "Overdue").sum()))
    st.metric("Completed impact", round(actions_df.loc[actions_df["status"] == "Complete", "mitigation_impact"].sum(), 2))

st.subheader("Risk register")
st.dataframe(risks_df, use_container_width=True, hide_index=True)

st.subheader("Action tracker")
status_filter = st.multiselect(
    "Filter by status",
    sorted(actions_df["status"].unique().tolist()),
    default=sorted(actions_df["status"].unique().tolist()),
)
filtered_actions = actions_df[actions_df["status"].isin(status_filter)]
st.dataframe(filtered_actions, use_container_width=True, hide_index=True)

st.subheader("Priority by risk category")
priority_chart = (
    risks_df.groupby("risk_category", as_index=False)["priority_level"]
    .max()
    .sort_values("priority_level", ascending=False)
)
fig1, ax1 = plt.subplots(figsize=(9, 4))
ax1.bar(priority_chart["risk_category"], priority_chart["priority_level"])
ax1.set_ylabel("Priority level")
ax1.set_xlabel("Risk category")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig1)

st.subheader("Action status summary")
status_chart = actions_df["status"].value_counts().sort_index()
fig2, ax2 = plt.subplots(figsize=(6, 4))
ax2.bar(status_chart.index, status_chart.values)
ax2.set_ylabel("Count")
ax2.set_xlabel("Status")
st.pyplot(fig2)

st.subheader("Mitigation effect by plan")
effect_chart = aggs_df.sort_values("mitigation_effect", ascending=False)
fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.bar(effect_chart["mitigation_plan"], effect_chart["mitigation_effect"])
ax3.set_ylabel("Completed mitigation effect")
ax3.set_xlabel("Mitigation plan")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig3)

st.subheader("Adjusted score by mitigation plan")
fig4, ax4 = plt.subplots(figsize=(10, 5))
ax4.bar(aggs_df["mitigation_plan"], aggs_df["adjusted_score"])
ax4.set_ylabel("Adjusted score")
ax4.set_xlabel("Mitigation plan")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig4)

st.subheader("Overdue actions")
overdue = actions_df[actions_df["status"] == "Overdue"].sort_values("deadline")
st.dataframe(overdue, use_container_width=True, hide_index=True)