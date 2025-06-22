import streamlit as st
import pandas as pd
import numpy as np
from utils.helper_functions import (
    render_global_toolbar,
    render_styled_bar_chart,
    render_dual_line_chart,
)

st.set_page_config(layout="wide")
st.markdown("<h2 style='text-align: center;'>Risk Decomposition</h2>", unsafe_allow_html=True)

# --- Toolbar ---
fund_list = ["Querido Global Macro Fund", "Querido Global Macro Fund II", "Querido Global Macro Fund III"]
strategy_list = ["Global Macro", "Quantitative Equity", "Systematic Macro", "Statistical Arbitrage"]
render_global_toolbar(fund_list, strategy_list)

# --- Global Inputs ---
fund = st.session_state.get("fund", "Fund A")
strategy = st.session_state.get("strategy", "Strategy X")
start_date = st.session_state.get("start_date")
end_date = st.session_state.get("end_date")
pit_date = st.session_state.get("pit_date")

# --- Control Toggles ---
view_level = st.radio("View", ["Composite", "Strategy"], horizontal=True)
risk_basis = st.radio("Risk Basis", ["Portfolio", "Benchmark", "Contribution to TE"], horizontal=True)

st.markdown("### PIT Risk Decomposition")

# --- PIT Risk Decomp ---
risk_types = ["Style", "Industry", "Market", "Currency", "Idiosyncratic"]
values = np.random.normal(1, 0.5, len(risk_types))
render_styled_bar_chart(
    title=f"{risk_basis} Risk by Factor",
    labels=risk_types,
    values=values,
    x_title="Risk Type",
    y_title="Value"
)

st.markdown("---")
st.markdown("### Risk Composition Over Time")

# --- Time Series Stacked Area Chart ---
dates = pd.date_range(start=start_date, end=end_date, periods=50)
df = pd.DataFrame({
    "Style": np.random.rand(50),
    "Industry": np.random.rand(50),
    "Market": np.random.rand(50),
    "Currency": np.random.rand(50),
    "Idiosyncratic": np.random.rand(50)
}, index=dates)
df = df.div(df.sum(axis=1), axis=0)  # normalize to 100%

st.area_chart(df)

st.markdown("---")
st.markdown("### Single Factor Time Series")

factor_choice = st.selectbox("Select Factor", ["Style", "Industry", "Market", "Currency", "Idiosyncratic"])
render_dual_line_chart(f"{factor_choice} Risk Over Time", df[factor_choice])
