import streamlit as st
from utils.helper_functions import render_markdown_from_file
import datetime

st.set_page_config(layout="wide")

# Title centered above
st.markdown("<h1 style='text-align: center;'>Querido Capital Management</h1>", unsafe_allow_html=True)

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
with st.sidebar:
    st.selectbox("Fund", fund_list, key="fund")
    st.selectbox("Strategy", strategy_list, key="strategy")
    st.date_input("PIT Date", value=datetime.date(2024, 12, 31), key="pit_date")
    st.date_input("Start Date", value=datetime.date(2020, 1, 1), key="start_date")
    st.date_input("End Date", value=datetime.date.today(), key="end_date")
# Horizontal input bar
# top1, top2, top3, top4, top5 = st.columns([1.2, 1.2, 1.2, 1.2, 1.2])
# with top1:
#     st.selectbox("Fund", fund_list, key="fund")
# with top2:
#     st.selectbox("Strategy", strategy_list, key="strategy")
# with top3:
#     st.date_input("PIT Date", value=datetime.date(2024, 12, 31), key="pit_date")
# with top4:
#     st.date_input("Start Date", value=datetime.date(2020, 1, 1), key="start_date")
# with top5:
#     st.date_input("End Date", value=datetime.date.today(), key="end_date")

# --- Two Columns Layout ---
col1, col2 = st.columns([1.5, 1])

with col1:
    st.markdown("<h1 style='text-align: left;'>Querido Capital Management</h1>", unsafe_allow_html=True)
    st.markdown("""
    Welcome to the **Querido Capital Management** platform. **Querido Capital Management** is a data-driven investment research and portfolio management firm. Our focus is on idea generation, investment research and strategy development.
    
    To navigate the platform, use the left sidebar.
    
    _Please reach out if you'd be interested in collaborating on research or would just like to connect!_
    [Check out my GitHub](https://github.com/lquerido/Querido-Asset-Management) or 
    [connect on LinkedIn](https://linkedin.com/in/liam-querido-aiaa-1235281b7/).
    """)

with col2:
    st.image("static/liam_querido.jpg")

st.markdown("---")

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

# with st.sidebar:
#     st.selectbox("Fund", fund_list, key="fund")
#     st.selectbox("Strategy", strategy_list, key="strategy")
#     st.date_input("PIT Date", value=datetime.date(2024, 12, 31), key="pit_date")
#     st.date_input("Start Date", value=datetime.date(2020, 1, 1), key="start_date")
#     st.date_input("End Date", value=datetime.date.today(), key="end_date")

render_markdown_from_file("pages/subview_utils/about_us/about.md")