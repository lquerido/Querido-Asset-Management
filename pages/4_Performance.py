import streamlit as st
import pandas as pd
import numpy as np
from utils.helper_functions import (
    render_global_toolbar,
    render_metric_grid,
    render_dual_line_chart,
    render_green_line_chart,
    render_green_bar_chart,
    render_drawdown_chart
)

st.set_page_config(layout="wide")
st.markdown("<h2 style='text-align: center;'>Performance Summary</h2>", unsafe_allow_html=True)

# --- Toolbar ---
fund_list = ["Querido Global Macro Fund", "Querido Global Macro Fund II", "Querido Global Macro Fund III"]
strategy_list = ["Global Macro", "Quantitative Equity", "Systematic Macro", "Statistical Arbitrage"]
render_global_toolbar(fund_list, strategy_list)

# --- Global Inputs ---
fund = st.session_state.get("fund", "Fund A")
strategy = st.session_state.get("strategy", "Strategy X")
pit_date = st.session_state.get("pit_date")
start_date = st.session_state.get("start_date")
end_date = st.session_state.get("end_date")

# --- Toggle: Composite vs Strategy ---
level = st.radio("Select Level", ["Composite", "Strategy"], horizontal=True)

# --- Summary Metrics ---
metrics = [
    ("Total Return", "14.8%"),
    ("Excess Return", "3.5%"),
    ("Volatility", "11.2%"),
    ("Sharpe Ratio", "1.21"),
    ("Tracking Error", "2.7%"),
    ("Information Ratio", "0.84"),
    ("Beta", "0.91"),
    ("Drawdown", "-6.4%"),
    ("Up Capture", "104%"),
    ("Down Capture", "93%"),
    ("Turnover", "18%")
]
render_metric_grid(metrics, columns=3)

st.markdown("---")

# --- Cumulative Returns ---
st.markdown("#### Cumulative Return (Indexed)")
dates = pd.date_range(start=start_date, end=end_date, periods=100)
portfolio = (1 + pd.Series(np.random.normal(0.001, 0.01, 100), index=dates)).cumprod()
benchmark = (1 + pd.Series(np.random.normal(0.0008, 0.01, 100), index=dates)).cumprod()
render_green_line_chart("Cumulative Return (Indexed)", [portfolio, benchmark], ["Portfolio", "Benchmark"])

st.markdown("---")

# --- Excess Return Bar Chart ---
st.markdown("#### Excess Return")
bar_freq = st.selectbox("Bar Chart Frequency", ["Monthly", "Quarterly", "Annual"], key="bar_freq")
bar_periods = {"Monthly": 12, "Quarterly": 8, "Annual": 5}[bar_freq]
bar_dates = pd.date_range(start=start_date, end=end_date, periods=bar_periods)
bar_series = pd.Series(np.random.normal(0.01, 0.02, bar_periods), index=bar_dates)
render_green_bar_chart(f"{bar_freq} Excess Return", bar_series.values, bar_series.index)

# --- Drawdown Chart ---
dd_freq = st.selectbox("Drawdown Frequency", ["Monthly", "Quarterly", "Annual"], key="dd_freq")
dd_series = pd.Series(np.random.normal(0.001, 0.01, 100), index=dates)  # Optionally vary by dd_freq
render_drawdown_chart(f"Excess Return Drawdowns ({dd_freq})", dd_series)

st.markdown("---")

# --- Rolling Metric Selector ---
st.markdown("#### Rolling Metric")
col1, col2 = st.columns(2)
with col1:
    metric = st.selectbox("Metric", ["Total Return", "Excess Return", "Volatility", "Sharpe Ratio", "Tracking Error",
                                     "Information Ratio", "Beta", "Drawdown", "Up Capture", "Down Capture", "Turnover"])
with col2:
    window = st.selectbox("Rolling Window (Months)", [3, 6, 12])
rolling = pd.Series(np.random.normal(0.8, 0.1, 100), index=dates)
render_dual_line_chart(f"Rolling {metric} ({window}-Month)", rolling)
