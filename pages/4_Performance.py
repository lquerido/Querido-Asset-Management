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
from utils.helper_functions import build_fund_registry

st.set_page_config(layout="wide")
st.markdown("<h2 style='text-align: center;'>Performance Summary</h2>", unsafe_allow_html=True)

# --- Toolbar ---
start_date = st.session_state.get("start_date", "2020-01-01")
end_date = st.session_state.get("end_date", "2024-12-31")
fund_registry = build_fund_registry(start_date, end_date)       # Todo: Why do we need start and end date?
render_global_toolbar(fund_registry)

# --- Global Inputs ---
# fund = st.session_state.get("fund", "Fund A")
# strategy = st.session_state.get("strategy", "Strategy X")
pit_date = st.session_state.get("pit_date")
# start_date = st.session_state.get("start_date")
# end_date = st.session_state.get("end_date")

# --- Toggle: Composite vs Strategy ---
st.radio(
    "Select Level",
    ["Composite", "Strategy"],
    horizontal=True,
    key="level"  # stores in session_state
)

# --- Summary Metrics ---
from app_state import get_performance_stats

# Assume these are set correctly in session state
fund = st.session_state.get("fund", "Querido Capital Fund 1")
level = st.session_state.get("level", "Composite")  # "Composite" or "Strategy"
strategy = st.session_state.get("strategy", "Global Macro")  # Needed if Strategy-level is selected

# Call once
all_stats = get_performance_stats(fund, start_date, end_date)

# Pick composite or strategy
stats = all_stats["composite"] if level == "Composite" else all_stats["strategies"][strategy]


metrics = [
    ("Total Return", f"{stats.total_return:.2%}"),
    ("Excess Return", f"{stats.excess_return:.2%}"),
    ("Volatility", f"{stats.volatility:.2%}"),
    ("Sharpe Ratio", f"{stats.sharpe:.2f}"),
    ("Tracking Error", f"{stats.tracking_error:.2%}"),
    ("Information Ratio", f"{stats.info_ratio:.2f}"),
    ("Beta", f"{stats.beta:.2f}"),
    ("Drawdown", f"{stats.max_drawdown:.2%}"),
    ("Up Capture", f"{stats.up_capture:.0%}"),
    ("Down Capture", f"{stats.down_capture:.0%}"),
    ("Turnover", f"{stats.turnover:.2%}"),
]
render_metric_grid(metrics, columns=3)

st.markdown("---")

# --- Cumulative Returns ---
st.markdown("#### Cumulative Return (Indexed)")
portfolio = (1 + stats.strategy_returns).cumprod()
benchmark = (1 + stats.benchmark_returns).cumprod()
dates = portfolio.index  # reuse actual dates
render_green_line_chart("Cumulative Return (Indexed)", [portfolio, benchmark], ["Portfolio", "Benchmark"])

st.markdown("---")

# --- Excess Return Bar Chart ---
st.markdown("#### Excess Return")
bar_freq = st.selectbox("Bar Chart Frequency", ["Monthly", "Quarterly", "Annual"], key="bar_freq")
bar_periods = {"Monthly": 12, "Quarterly": 8, "Annual": 5}[bar_freq]
excess = stats.strategy_returns - stats.benchmark_returns
# excess.index = pd.to_datetime(excess.index)
# excess = excess.sort_index()
bar_series = excess.resample({'Monthly': 'M', 'Quarterly': 'Q', 'Annual': 'A'}[bar_freq]).sum()
render_green_bar_chart(f"{bar_freq} Excess Return", bar_series.values, bar_series.index)

# --- Drawdown Chart ---
dd_freq = st.selectbox("Drawdown Frequency", ["Monthly", "Quarterly", "Annual"], key="dd_freq")

# Map selection to Pandas frequency string
freq_map = {
    "Monthly": "M",
    "Quarterly": "Q",
    "Annual": "A"
}
resampled_returns = stats.strategy_returns.resample(freq_map[dd_freq]).apply(lambda x: (1 + x).prod() - 1)
cum_return = (1 + resampled_returns).cumprod()
dd_series = cum_return / cum_return.cummax() - 1

render_drawdown_chart(f"Excess Return Drawdowns ({dd_freq})", dd_series)

# --- Rolling Metric Selector ---
st.markdown("#### Rolling Metric")
col1, col2 = st.columns(2)
with col1:
    # metric = st.selectbox("Metric", ["Total Return", "Excess Return", "Volatility", "Sharpe Ratio", "Tracking Error",
    #                                  "Information Ratio", "Beta", "Drawdown", "Up Capture", "Down Capture", "Turnover"])
    metric = st.selectbox("Metric", ["Volatility", "Sharpe Ratio", "Information Ratio"])
with col2:
    window = st.selectbox("Rolling Window (Months)", [3, 6, 12])
metric_map = {
    "Volatility": stats.rolling_metrics[f"{window}M"]["Volatility"],
    "Sharpe Ratio": stats.rolling_metrics[f"{window}M"]["Sharpe Ratio"],
    # "Tracking Error": stats.rolling_metrics[f"{window}M"]["Tracking Error"],
    "Information Ratio": stats.rolling_metrics[f"{window}M"]["Information Ratio"],
}
rolling = metric_map.get(metric)
render_dual_line_chart(f"Rolling {metric} ({window}-Month)", rolling)
