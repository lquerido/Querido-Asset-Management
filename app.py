# Base Dashboard Template for Querido Capital Management

import streamlit as st
import pandas as pd
import numpy as np
import importlib
from view_config import VIEW_STRUCTURE, VIEW_MODULES

# --- DUMMY DATA SETUP ---
def load_dummy_data():
    dates = pd.date_range(start="2022-01-01", periods=100, freq="D")
    prices = np.cumsum(np.random.randn(100)) + 100
    dummy_df = pd.DataFrame({"Date": dates, "Price": prices})
    return dummy_df

data = load_dummy_data()

# --- SIDEBAR CONTROLS ---
def render_sidebar(view):
    if view == "Performance Summary":
        st.sidebar.subheader("Performance Summary")
        st.sidebar.button("Download PM Update")
    elif view == "Detailed Investment Performance Analysis":
        st.sidebar.subheader("Portfolio Analytics")
        st.sidebar.radio("Select Analysis", [
            "Trade-by-Trade Analysis",
            "Time-Weighted Returns",
            "Portfolio Composition",
            "Portfolio Holdings",
            "Portfolio Risk",
            "Attribution Analysis"
        ])
        st.sidebar.subheader("Datasets")
        st.sidebar.radio("Data Type", ["MACRO", "SECURITIES"])
    elif view == "Investment Research":
        st.sidebar.subheader("Research Library")
        st.sidebar.radio("Category", ["Macro", "Equities"])
    elif view == "About Us":
        st.sidebar.markdown("[LinkedIn](https://linkedin.com)")
        st.sidebar.markdown("[GitHub](https://github.com)")
        st.sidebar.radio("Learn More", [
            "Our Strategies",
            "Capital Allocation",
            "Dashboard Logic"
        ])

# --- MAIN VIEW RENDERING ---
def render_view(view):
    if view == "Performance Summary":
        st.header("Performance Summary")
        st.write("Key metrics snapshot")
        st.line_chart(data.set_index("Date"))

    elif view == "Detailed Investment Performance Analysis":
        st.header("Detailed Investment Performance Analysis")
        st.write("Placeholder for trade analytics and risk breakdown")

    elif view == "Investment Research":
        st.header("Investment Research")
        st.write("Library of research papers")

    elif view == "About Us":
        st.header("About Querido Capital Management")
        st.markdown("""
        Learn about our mission, team, and investment strategies. 
        More information on the dashboard logic and methodology is available.
        """)

# --- Navigation ---
main_views = list(VIEW_STRUCTURE.keys())
cols = st.columns(len(main_views))

if "selected_view" not in st.session_state:
    st.session_state.selected_view = main_views[0]  # default

for i, view_name in enumerate(main_views):
    if cols[i].button(view_name):
        st.session_state.selected_view = view_name

selected_view = st.session_state.selected_view

# --- Subview Navigation ---
subviews = VIEW_STRUCTURE.get(selected_view, [])
selected_subview = st.sidebar.radio("Select View", subviews) if subviews else None

# --- Load View Dynamically ---
module_path = VIEW_MODULES.get(selected_view)
if module_path:
    view_module = importlib.import_module(module_path)
    view_module.render(selected_subview)
else:
    st.error("View not implemented.")
