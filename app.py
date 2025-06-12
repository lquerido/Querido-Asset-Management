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
from views.performance_summary import render_summary, render_risk_and_performance, render_exposures_and_positioning
from views.detailed_analysis import render_attribution

#
# def load_config(path="config.yaml"):
#     with open(path, "r") as f:
#         return yaml.safe_load(f)
#
# def run_simulation(config):
#     tickers = config["tickers"]
#     start = config["start"]
#     end = config["end"]
#     vol_data = GetSeries(ticker=tickers, start=start, end=end).fetch_volatility()
#
#     strategies = {}
#     for name, strat_cfg in config["strategies"].items():
#         strategy_cls = globals()[strat_cfg["class"]]
#         allocator_cls = globals()[strat_cfg["allocator"]]
#         strat = InitialiseStrategy(
#             strategy_cls=strategy_cls,
#             allocator_cls=allocator_cls,
#             tickers=tickers,
#             start=start,
#             end=end,
#             strategy_kwargs=strat_cfg.get("strategy_kwargs", {}),
#             allocator_kwargs={"vol_data": vol_data}
#         )
#         strategies[name] = (strat, strat_cfg["weight"])
#
#     ensemble = StrategyEnsemble(strategies)
#
#     benchmark_cfg = config["benchmark"]
#     benchmark = InitialiseStrategy(
#         strategy_cls=globals()[benchmark_cfg["class"]],
#         allocator_cls=globals()[benchmark_cfg["allocator"]],
#         tickers=benchmark_cfg["ticker"],
#         start=start,
#         end=end
#     )
#
#     stats = main(
#         tickers,
#         ensemble,
#         benchmark_ticker=benchmark_cfg["ticker"],
#         benchmark_strat=benchmark,
#         start_date=start,
#         end_date=end,
#         slippage=config["slippage"],
#         commission=config["commission"]
#     )
#     return stats
#
# # --- SIDEBAR CONTROLS ---
# def render_sidebar(view):
#     if view == "Performance Summary":
#         st.sidebar.subheader("Performance Summary")
#         st.sidebar.button("Download PM Update")
#     elif view == "Detailed Investment Performance Analysis":
#         st.sidebar.subheader("Portfolio Analytics")
#         st.sidebar.radio("Select Analysis", [
#             "Trade-by-Trade Analysis",
#             "Time-Weighted Returns",
#             "Portfolio Composition",
#             "Portfolio Holdings",
#             "Portfolio Risk",
#             "Attribution Analysis"
#         ])
#         st.sidebar.subheader("Datasets")
#         st.sidebar.radio("Data Type", ["MACRO", "SECURITIES"])
#     elif view == "Investment Research":
#         st.sidebar.subheader("Research Library")
#         st.sidebar.radio("Category", ["Macro", "Equities"])
#     elif view == "About Us":
#         st.sidebar.markdown("[LinkedIn](https://linkedin.com)")
#         st.sidebar.markdown("[GitHub](https://github.com)")
#         st.sidebar.radio("Learn More", [
#             "Our Strategies",
#             "Capital Allocation",
#             "Dashboard Logic"
#         ])
#
#
# # --- MAIN VIEW RENDERING ---
# def render_view(view):
#     if view == "Performance Summary":
#         st.header("Performance Summary")
#         # if st.button("Run Backtest"):
#         #     config = load_config()
#         #     equity, returns = run_simulation(config)
#         #
#         #     st.session_state["backtest_results"] = {
#         #         "equity": equity,
#         #         "returns": returns,
#         #     }
#         #
#         # if "backtest_results" in st.session_state:
#         #     st.line_chart(st.session_state["backtest_results"]["equity"])
#
#     elif view == "Detailed Investment Performance Analysis":
#         st.header("Detailed Investment Performance Analysis")
#         st.write("Placeholder for trade analytics and risk breakdown")
#
#     elif view == "Investment Research":
#         st.header("Investment Research")
#         st.write("Library of research papers")
#
#     elif view == "About Us":
#         st.header("About Querido Capital Management")
#         st.markdown("""
#         Learn about our mission, team, and investment strategies.
#         More information on the dashboard logic and methodology is available.
#         """)
#
# # --- Navigation ---
# main_views = list(VIEW_STRUCTURE.keys())
# cols = st.columns(len(main_views))
#
# @st.cache_data
# def get_backtest_results():
#     config = load_config()
#     return run_simulation(config)
#
# if "backtest_results" not in st.session_state:
#     st.session_state["backtest_results"] = get_backtest_results()
#
# if st.sidebar.button("Home"):
#     selected_view = "Home"
#     selected_subview = None
#
# with st.sidebar:
#     st.title("Querido Capital")
#
#     # Flatten all subviews with their view names
#     subview_options = [
#         (view_name, subview)
#         for view_name, subviews in VIEW_STRUCTURE.items()
#         for subview in subviews
#     ]
#
#     # Display subviews grouped by headings, but select only one
#     st.markdown("### Select an Option")
#
#     # Create readable labels like "Performance Summary - PM Update"
#     labels = [f"{view} - {sub}" for view, sub in subview_options]
#     selection = st.radio("Navigation", labels)
#
#     # Parse selection into view and subview
#     selected_view, selected_subview = next(
#         (view, sub) for view, sub in subview_options if f"{view} - {sub}" == selection
#     )
#
# # --- Load View Dynamically ---
# module_path = VIEW_MODULES.get(selected_view)
# if module_path:
#     view_module = importlib.import_module(module_path)
#     view_module.render(selected_subview)
# else:
#     st.error("View not implemented.")



import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")  # ✅ makes use of full browser width

# Optional: extra styling tweaks
st.markdown("""
    <style>
        /* Hide Streamlit default header, menu, footer */
        #MainMenu, header, footer {
            visibility: hidden;
            height: 0px;
        }
        /* Force main content up */
        .appview-container {
            padding-top: 0 !important;
            margin-top: -5rem !important;
        }
        /* Reduce top padding inside the sidebar */
        section[data-testid="stSidebar"] > div:first-child {
            padding-top: 2rem !important;
            margin-top: 2rem !important;
        }
    </style>
""", unsafe_allow_html=True)


# --- Sidebar Navigation ---
VIEW_STRUCTURE = {
    "Simplified Portfolio Analysis": ["Summary", "Risk", "Exposure"],
    "Advanced Portfolio Analysis": ["Attribution", "Trades", "Strategies"],
}

all_options = []
option_map = {}
for section, subviews in VIEW_STRUCTURE.items():
    for sub in subviews:
        label = f"{section} > {sub}"
        all_options.append(label)
        option_map[label] = (section, sub)

button_style = """
    <style>
        .sidebar-button {
            width: 100%;
            text-align: left;
            background-color: #f0f2f6;
            cursor: pointer;
            font-size: 1rem;
        }
        .sidebar-button:hover {
            background-color: #e0e0e0;
        }
    </style>
"""
st.markdown(button_style, unsafe_allow_html=True)

with st.sidebar:
    st.title("Querido Capital")

    if "selected_view" not in st.session_state:
        st.session_state.selected_view = list(VIEW_STRUCTURE.items())[0][1][0]

    for section, subviews in VIEW_STRUCTURE.items():
        st.markdown(f"#### {section}")
        for sub in subviews:
            form_key = f"form_{sub}"
            button_key = f"btn_{sub}"
            with st.form(form_key):
                submitted = st.form_submit_button(sub, use_container_width=True)
                if submitted:
                    st.session_state.selected_view = sub

selected_subview = st.session_state.selected_view

# --- Dummy Data ---
def dummy_series(n=100, scale=1):
    return pd.Series(np.cumsum(np.random.randn(n) * scale))

def dummy_returns(n=100):
    return pd.Series(np.random.randn(n) / 100)

# --- Render View Logic ---
def render(subview):
    # st.title(subview)

    if subview == "Summary":
        render_summary()

    elif subview == "Risk":
        render_risk_and_performance()

    elif subview == "Exposure":
        render_exposures_and_positioning()

    elif subview == "Attribution":
        render_attribution()

    elif subview == "Trades":
        st.subheader("Trade Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Trades", "243")
        col2.metric("Win Rate", "62%")
        col3.metric("Avg Return per Trade", "1.2%")

        col4, col5, col6 = st.columns(3)
        col4.metric("Avg Holding Period", "14 days")
        col5.metric("Largest Gain", "7.4%")
        col6.metric("Largest Loss", "-5.9%")

        st.markdown("### Trade Return Distribution")
        fig = px.histogram(np.random.randn(200), nbins=40, title="Trade Return Histogram")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Trade Log")
        trade_log = pd.DataFrame({
            "Date": pd.date_range(end=pd.Timestamp.today(), periods=10),
            "Instrument": [f"Asset {i}" for i in range(10)],
            "Buy/Sell": np.random.choice(["Buy", "Sell"], 10),
            "Signal": np.random.choice(["Momentum", "Reversion"], 10),
            "Leverage": np.round(np.random.uniform(1.0, 2.0, 10), 2),
            "Size": np.random.randint(1000, 5000, 10),
            "P&L": np.round(np.random.randn(10), 2)
        })
        st.dataframe(trade_log)

    elif subview == "Strategies":
        st.subheader("Signal Attribution")
        st.write("### P&L by Signal")
        st.bar_chart(pd.Series(np.random.randn(5), index=["Momentum", "Mean Reversion", "Carry", "Value", "Quality"]))

        st.write("### Heatmap: Signal x Trade Return")
        heatmap_data = pd.DataFrame(np.random.randn(5, 10), index=["Momentum", "Reversion", "Carry", "Value", "Quality"])
        st.dataframe(heatmap_data.style.background_gradient(cmap='RdYlGn'))

    else:
        st.info("Select a valid subview.")

# --- Call Renderer ---
render(selected_subview)
