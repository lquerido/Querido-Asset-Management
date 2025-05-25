import streamlit as st
from pathlib import Path
import json
import pandas as pd
from backtest import PriceData, SignalStrategy, TransactionCostModel, BacktestEngine, PerformanceStats
import matplotlib.pyplot as plt

# Cache price data
@st.cache_data
def get_price_data():
    from backtest import PriceData  # or adjust the import path
    return PriceData("SPY", "2020-01-01", "2024-12-31").data

st.set_page_config(page_title="Quant Dashboard", layout="wide")

st.sidebar.title("Navigation")
tabs = [
    "Performance Summary",
    "Strategy Logic",
    "Data Workflow",
    "Performance Attribution",
    "Risk & Objectives",
    "Capital Allocation",
    "Investment Philosophy",
    "Research & Commentary",
    "PM Letters",
    "About"
]
selection = st.sidebar.radio("Go to", tabs)

if selection == "Performance Summary":
    st.title("📈 Performance Summary")

    # Run backtest
    prices = PriceData("SPY", "2020-01-01", "2024-12-31").data
    price_series = prices["Price"]  # Ensure this is a Series
    strategy = SignalStrategy()
    cost_model = TransactionCostModel()
    engine = BacktestEngine(price_series, strategy, cost_model)
    equity_curve, returns = engine.run()
    stats = PerformanceStats(equity_curve, returns).compute()

    # Plot equity curve
    st.subheader("Equity Curve")
    fig, ax = plt.subplots()
    equity_curve.plot(ax=ax)
    ax.set_ylabel("Portfolio Value ($)")
    ax.set_title("Equity Curve")
    st.pyplot(fig)

    # Show stats
    st.subheader("Performance Statistics")
    stats_df = pd.DataFrame(stats, index=["Metrics"]).T
    st.table(stats_df)

elif selection == "Strategy Logic":
    st.title("🧠 Strategy Logic & Assumptions")
    st.markdown(Path("docs/strategy.md").read_text())

elif selection == "Data Workflow":
    st.title("🔄 Data & Workflow Overview")
    st.markdown(Path("docs/data_workflow.md").read_text())

elif selection == "Performance Attribution":
    st.title("🧮 Performance Attribution")
    st.markdown(Path("docs/performance_attribution.md").read_text())

elif selection == "Risk & Objectives":
    st.title("🎯 Risk Objectives & Evaluation")
    st.markdown(Path("docs/risk_objectives.md").read_text())

elif selection == "Capital Allocation":
    st.title("📊 Capital Allocation Framework")
    st.markdown(Path("docs/capital_allocation.md").read_text())

elif selection == "Investment Philosophy":
    st.title("🧭 Investment Philosophy & Mandate")
    st.markdown(Path("investment_philosophy.md").read_text())

elif selection == "Research & Commentary":
    st.title("📰 Research & Market Commentary")
    st.markdown(Path("docs/research.md").read_text())

elif selection == "PM Letters":
    st.title("📬 PM Letters to Investors")
    st.markdown(Path("docs/pm_letters.md").read_text())

elif selection == "About":
    st.title("👤 About Me")
    st.markdown(Path("docs/about.md").read_text())
