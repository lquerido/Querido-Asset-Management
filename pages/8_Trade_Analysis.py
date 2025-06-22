import streamlit as st
import pandas as pd
import numpy as np
from utils.helper_functions import render_dual_line_chart, render_global_toolbar

# --- Sidebar ---
fund_list = [
    "Querido Global Macro Fund",
    "Querido Global Macro Fund II",
    "Querido Global Macro Fund III",
]
strategy_list = [
    "Global Macro",
    "Quantitative Equity",
    "Systematic Macro",
    "Statistical Arbitrage",
]
render_global_toolbar(fund_list, strategy_list)

st.markdown("<h2 style='text-align: center;'>Rolling Statistics</h2>", unsafe_allow_html=True)

# --- Global Inputs ---
fund = st.session_state.get("fund", "Fund A")
strategy = st.session_state.get("strategy", "Strategy X")
start_date = st.session_state.get("start_date")
end_date = st.session_state.get("end_date")

# --- Dropdowns for Metric and Level ---
metric = st.selectbox("Select Rolling Metric", [
    "Volatility", "Beta", "Sharpe Ratio", "Tracking Error", "Information Ratio"
])
level = st.radio("View For", ["Composite", "Strategy"])

# --- Simulated Rolling Time Series ---
dates = pd.date_range(start=start_date, end=end_date, periods=60)
composite_series = pd.Series(np.random.normal(0.8, 0.1, len(dates)), index=dates)
strategy_series = pd.Series(np.random.normal(0.75, 0.15, len(dates)), index=dates)

# --- Render Line Chart ---
if level == "Composite":
    render_dual_line_chart(f"Composite {metric} (Rolling)", composite_series)
else:
    render_dual_line_chart(f"{strategy} {metric} (Rolling)", strategy_series)
