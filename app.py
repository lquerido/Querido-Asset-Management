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
import yaml

def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def run_simulation(config):
    tickers = config["tickers"]
    start = config["start"]
    end = config["end"]
    vol_data = GetSeries(ticker=tickers, start=start, end=end).fetch_volatility()

    strategies = {}
    for name, strat_cfg in config["strategies"].items():
        strategy_cls = globals()[strat_cfg["class"]]
        allocator_cls = globals()[strat_cfg["allocator"]]
        strat = InitialiseStrategy(
            strategy_cls=strategy_cls,
            allocator_cls=allocator_cls,
            tickers=tickers,
            start=start,
            end=end,
            strategy_kwargs=strat_cfg.get("strategy_kwargs", {}),
            allocator_kwargs={"vol_data": vol_data}
        )
        strategies[name] = (strat, strat_cfg["weight"])

    ensemble = StrategyEnsemble(strategies)

    benchmark_cfg = config["benchmark"]
    benchmark = InitialiseStrategy(
        strategy_cls=globals()[benchmark_cfg["class"]],
        allocator_cls=globals()[benchmark_cfg["allocator"]],
        tickers=benchmark_cfg["ticker"],
        start=start,
        end=end
    )

    stats = main(
        tickers,
        ensemble,
        benchmark_ticker=benchmark_cfg["ticker"],
        benchmark_strat=benchmark,
        start_date=start,
        end_date=end,
        slippage=config["slippage"],
        commission=config["commission"]
    )
    return stats

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
        # if st.button("Run Backtest"):
        #     config = load_config()
        #     equity, returns = run_simulation(config)
        #
        #     st.session_state["backtest_results"] = {
        #         "equity": equity,
        #         "returns": returns,
        #     }
        #
        # if "backtest_results" in st.session_state:
        #     st.line_chart(st.session_state["backtest_results"]["equity"])

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

@st.cache_data
def get_backtest_results():
    config = load_config()
    return run_simulation(config)

if "backtest_results" not in st.session_state:
    st.session_state["backtest_results"] = get_backtest_results()

if st.sidebar.button("Home"):
    selected_view = "Home"
    selected_subview = None

with st.sidebar:
    st.title("Querido Capital")

    # Flatten all subviews with their view names
    subview_options = [
        (view_name, subview)
        for view_name, subviews in VIEW_STRUCTURE.items()
        for subview in subviews
    ]

    # Display subviews grouped by headings, but select only one
    st.markdown("### Select an Option")

    # Create readable labels like "Performance Summary - PM Update"
    labels = [f"{view} - {sub}" for view, sub in subview_options]
    selection = st.radio("Navigation", labels)

    # Parse selection into view and subview
    selected_view, selected_subview = next(
        (view, sub) for view, sub in subview_options if f"{view} - {sub}" == selection
    )

# --- Load View Dynamically ---
module_path = VIEW_MODULES.get(selected_view)
if module_path:
    view_module = importlib.import_module(module_path)
    view_module.render(selected_subview)
else:
    st.error("View not implemented.")
