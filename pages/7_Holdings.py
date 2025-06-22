import streamlit as st
import pandas as pd
import numpy as np
from utils.helper_functions import render_global_toolbar, render_dual_line_chart

st.set_page_config(layout="wide")
st.markdown("<h2 style='text-align: center;'>Trade Analysis</h2>", unsafe_allow_html=True)

# --- Toolbar ---
fund_list = ["Querido Global Macro Fund", "Querido Global Macro Fund II", "Querido Global Macro Fund III"]
strategy_list = ["Global Macro", "Quantitative Equity", "Systematic Macro", "Statistical Arbitrage"]
render_global_toolbar(fund_list, strategy_list)

# --- Inputs ---
fund = st.session_state.get("fund")
strategy = st.session_state.get("strategy")
pit_date = st.session_state.get("pit_date")
start_date = st.session_state.get("start_date")
end_date = st.session_state.get("end_date")

# --- Duration Buckets ---
buckets = ["<1 Month", "1–3 Months", "3–6 Months", "6–12 Months", ">1 Year"]
num_stocks = np.random.randint(10, 50, len(buckets))
weights = np.random.uniform(1, 10, len(buckets)).round(2)
returns = np.random.normal(0.5, 0.2, len(buckets)).round(2)

df = pd.DataFrame({
    "Holding Period": buckets,
    "Number of Stocks": num_stocks,
    "Total Weight (%)": weights,
    "Relative Return (%)": returns
}).set_index("Holding Period")

st.markdown("### Holdings by Duration")
st.dataframe(df)

# --- Chart Selection ---
st.markdown("---")
st.markdown("### Time Series by Holding Duration")

col1, col2 = st.columns(2)
with col1:
    metric = st.selectbox("Metric", ["Number of Stocks", "Total Weight (%)", "Relative Return (%)"])
with col2:
    duration = st.selectbox("Holding Period", buckets)

# --- Dummy Time Series ---
dates = pd.date_range(start=start_date, end=end_date, periods=50)
series = pd.Series(np.random.normal(5, 1, len(dates)), index=dates)

render_dual_line_chart(f"{metric} for {duration}", series)
