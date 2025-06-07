# Base Dashboard Template for Querido Capital Management

import streamlit as st
import pandas as pd
import numpy as np
import importlib
from view_config import VIEW_STRUCTURE, VIEW_MODULES
from datasets.GetSeries import GetSeries
from strategies.signal_generation.MomentumStrategy import MomentumStrategy
from strategies.signal_generation.MeanReversionStrategy import MeanReversionStrategy
from strategies.signal_generation.BuyAndHoldStrategy import BuyAndHoldStrategy
from strategies.allocations.VolatilityScaledAllocator import VolatilityScaledAllocator
from strategies.allocations.EqualWeightAllocator import EqualWeightAllocator
from strategies.StrategyEnsemble import StrategyEnsemble
from strategies.InitialiseStrategy import InitialiseStrategy
from strategies.rebalancing.NaiveFullRebalancer import NaiveFullRebalancer
from stats.PerformanceStats import PerformanceStats
from simulation.StrategyExecution import main

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
        if st.button("Run Backtest"):
            tickers = ["AAPL", "MSFT", "GOOG", "TSLA"]
            start = "2020-01-01"
            end = "2024-12-31"
            vol_data = GetSeries(ticker=tickers, start=start, end=end).fetch_volatility()

            mean_rev = InitialiseStrategy(
                strategy_cls=MeanReversionStrategy,
                allocator_cls=VolatilityScaledAllocator,
                tickers=tickers,
                start=start,
                end=end,
                strategy_kwargs={"lookback": 20, "bound": 2},
                allocator_kwargs={"vol_data": vol_data}
            )
            ensemble = StrategyEnsemble({"mean_reversion": (mean_rev, 1.0)})

            benchmark = InitialiseStrategy(
                strategy_cls=BuyAndHoldStrategy,
                allocator_cls=EqualWeightAllocator,
                tickers="SPY",
                start=start,
                end=end
            )

            equity, returns = main(
                tickers,
                ensemble,
                benchmark_ticker="SPY",
                benchmark_strat=benchmark,
                start_date=start,
                end_date=end,
                slippage=0.001,
                commission=0.0005
            )

            st.session_state["backtest_results"] = {
                "equity": equity,
                "returns": returns,
            }

            # Show results if available
        if "backtest_results" in st.session_state:
            st.line_chart(st.session_state["backtest_results"]["equity"])

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
