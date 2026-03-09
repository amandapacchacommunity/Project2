import pandas as pd
import streamlit as st

st.set_page_config(page_title="Enterprise Risk Dashboard", layout="wide")

st.title("Enterprise Risk Dashboard")
st.write("Synthetic risk register analytics project")

# Load dataset
df = pd.read_csv("data/synthetic_risk_register.csv")

# Convert numbers
df["impact_level"] = pd.to_numeric(df["impact_level"], errors="coerce")
df["probability_level"] = pd.to_numeric(df["probability_level"], errors="coerce")

# KPI Metrics
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Risks", len(df))
col2.metric("Average Impact", round(df["impact_level"].mean(), 2))
col3.metric("Average Probability", round(df["probability_level"].mean(), 2))

# Risk Category Chart
st.subheader("Risks by Category")

risk_counts = df["risk_category"].value_counts()

st.bar_chart(risk_counts)

# Risk Table
st.subheader("Risk Register")

st.dataframe(df)