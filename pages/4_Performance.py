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
from app_state import get_performance_stats
stats = get_performance_stats()

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
cum_return = (1 + stats.strategy_returns).cumprod()
dd_series = cum_return / cum_return.cummax() - 1
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
rolling_map = {
    "Volatility": stats.rolling_volatility,
    "Sharpe Ratio": stats.rolling_sharpe,
    "Information Ratio": stats.rolling_ir,
}
rolling = rolling_map.get(metric, stats.rolling_sharpe)  # default fallback
render_dual_line_chart(f"Rolling {metric} ({window}-Month)", rolling)
