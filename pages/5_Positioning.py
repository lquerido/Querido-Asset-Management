import streamlit as st
import pandas as pd
import numpy as np
from utils.helper_functions import (
    render_global_toolbar,
    render_dual_line_chart,
    render_styled_bar_chart,
)

st.set_page_config(layout="wide")
st.markdown("<h2 style='text-align: center;'>Portfolio Positioning</h2>", unsafe_allow_html=True)

# --- Toolbar ---
fund_list = ["Querido Global Macro Fund", "Querido Global Macro Fund II", "Querido Global Macro Fund III"]
strategy_list = ["Global Macro", "Quantitative Equity", "Systematic Macro", "Statistical Arbitrage"]
render_global_toolbar(fund_list, strategy_list)

# --- Inputs ---
fund = st.session_state.get("fund", "Fund A")
strategy = st.session_state.get("strategy", "Strategy X")
start_date = st.session_state.get("start_date")
end_date = st.session_state.get("end_date")
pit_date = st.session_state.get("pit_date")

level = st.radio("View Level", ["Composite", "Strategy"], horizontal=True)

# --- Section 1: PIT Strategy Metrics (Composite Only) ---
if level == "Composite":
    st.markdown("#### Strategy PIT Metrics")
    df_pit = pd.DataFrame({
        "Strategy": ["Momentum", "Value", "Quality", "Macro"],
        "Weight": np.random.rand(4).round(2),
        "Beta": np.random.rand(4).round(2),
        "Tracking Error": np.random.rand(4).round(2),
        "Contribution to TE": np.random.rand(4).round(2)
    }).set_index("Strategy")
    st.dataframe(df_pit.style.background_gradient(cmap="Blues"), use_container_width=True)
    st.markdown("---")

# --- Section 2: Time Series Strategy Weights ---
st.markdown("#### Strategy Allocation Over Time")
dates = pd.date_range(start=start_date, end=end_date, periods=50)
strategies = ["Momentum", "Value", "Quality", "Macro"]
data = {name: np.random.dirichlet(np.ones(4), size=50)[:, i] for i, name in enumerate(strategies)}
df_weights = pd.DataFrame(data, index=dates)

render_dual_line_chart("Strategy Allocation", df_weights[strategies[0]])
# optionally loop or allow user to select strategy to plot individually

st.markdown("---")

# --- Section 3: Valuation Time Series ---
st.markdown("#### Valuation Metrics")
metric = st.selectbox("Valuation Metric", ["P/E", "P/B", "P/CF"])
val_series = pd.Series(np.random.normal(15, 2, 50), index=dates)
render_dual_line_chart(f"{level} {metric}", val_series)
st.markdown("---")

# --- Section 4: Sector & Geography Exposure ---
st.markdown("#### Sector and Geographic Exposure")
exposure_type = st.radio("Exposure Type", ["Sector", "Market Cap", "Geography", "Currency"], horizontal=True)
categories = [f"{exposure_type} {i+1}" for i in range(5)]
portfolio_exp = np.random.rand(5)
benchmark_exp = np.random.rand(5)
active_exp = portfolio_exp - benchmark_exp

df_exp = pd.DataFrame({
    "Portfolio": portfolio_exp,
    "Benchmark": benchmark_exp,
    "Active": active_exp
}, index=categories)

st.dataframe(df_exp.style.background_gradient(cmap="Oranges"), use_container_width=True)

render_styled_bar_chart(f"Active {exposure_type} Exposure", categories, active_exp, x_title=exposure_type, y_title="Active Weight")
st.markdown("---")

# --- Section 5: Brinson Attribution ---
st.markdown("#### Brinson Attribution")
col1, col2 = st.columns(2)
with col1:
    brinson_type = st.selectbox("Attribution Type", ["Sector", "Geography", "Market Cap", "Currency"])
with col2:
    period = st.selectbox("Period", ["1 Month", "1 Quarter", "12 Months"])
allocation = np.random.normal(0, 0.5, 5)
selection = np.random.normal(0, 0.5, 5)
interaction = np.random.normal(0, 0.2, 5)
total = allocation + selection + interaction

df_brinson = pd.DataFrame({
    "Allocation": allocation,
    "Selection": selection,
    "Interaction": interaction,
    "Total": total
}, index=[f"{brinson_type} {i+1}" for i in range(5)])

st.dataframe(df_brinson.style.background_gradient(cmap="Greens"), use_container_width=True)
render_styled_bar_chart("Total Attribution Effect", df_brinson.index.tolist(), df_brinson["Total"].values,
                        x_title=brinson_type, y_title="Total Effect")

st.markdown("---")

# --- Section 6: Risk Decomposition ---
st.markdown("#### Factor/Idiosyncratic Risk Decomposition")
risk_types = ["Style", "Industry", "Market", "Currency", "Idiosyncratic"]
contributions = np.random.rand(len(risk_types))
render_styled_bar_chart("Risk Contribution", risk_types, contributions, x_title="Risk Type", y_title="Contribution")
