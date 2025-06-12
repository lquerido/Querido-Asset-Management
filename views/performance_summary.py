import streamlit as st
import pandas as pd
import plotly.express as px

# def render(subview):
#     if subview == "Performance Analytics":
#         st.header("Composite Portfolio Performance")
#
#         if "backtest_results" in st.session_state:
#             results = st.session_state["backtest_results"]
#
#             # Key Metrics
#             st.subheader("Key Metrics")
#             stats_df = pd.DataFrame(results["performance_stats"], index=["Value"]).T
#             st.table(stats_df)
#
#             # Equity Curves
#             st.subheader("Equity Curves")
#             equity_df = pd.DataFrame({
#                 "Strategy": results["strategy_equity"],
#                 "Benchmark": results["benchmark_equity"]
#             })
#             st.line_chart(equity_df)
#
#             # Returns
#             st.subheader("Returns")
#             returns_df = pd.DataFrame({
#                 "Strategy Returns": results["strategy_returns"],
#                 "Benchmark Returns": results["benchmark_returns"]
#             })
#             st.line_chart(returns_df)
#
#             # Returns Histogram
#             st.subheader("Return Distribution (Strategy)")
#             fig = px.histogram(results["strategy_returns"], nbins=50, title="Strategy Return Distribution")
#             st.plotly_chart(fig, use_container_width=True)
#
#             # Trade Log (Optional)
#             st.subheader("Trade Log")
#             st.dataframe(pd.DataFrame(results["trade_log"]))
#
#             # Execution Log (Optional)
#             with st.expander("Execution Log"):
#                 st.dataframe(pd.DataFrame(results["execution_log"]))
#
#         else:
#             st.info("Run a backtest first.")


import pandas as pd
import numpy as np
import datetime


def dummy_series(n=100, scale=1):
    dates = pd.date_range(end=pd.Timestamp.today(), periods=n)
    data = np.cumsum(np.random.randn(n) * scale)
    return pd.Series(data, index=dates)


def render_summary():
    # --- Centered Title ---
    st.markdown("<h2 style='text-align: center;'>Summary</h2>", unsafe_allow_html=True)

    # --- Date Filters Below Title ---
    inception_date = datetime.date(2020, 1, 1)
    today = datetime.date.today()

    col1, col2 = st.columns([1, 1])
    with col1:
        start_date = st.date_input("Start Date", value=inception_date)
    with col2:
        end_date = st.date_input("End Date", value=today)
    # --- Metric Cards in a Row ---
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        for col, label, value in zip(
                [col1, col2, col3, col4],
                ["Total Investment", "Most Frequent", "Mean Investment", "Rating"],
                ["2.48B", "847,300", "4.94M", "3.5K"]
        ):
            col.markdown(f"""
                <div style="
                    background-color: #f0f2f6;
                    border-radius: 12px;
                    padding: 1rem;
                    text-align: center;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
                ">
                    <div style="font-size: 1.8rem; font-weight: 600; color: #333;">{value}</div>
                    <div style="font-size: 0.9rem; color: #666;">{label}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # --- Chart Row 1 ---
    with st.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("#### Investment by Region")
            st.line_chart(dummy_series())
        with col2:
            st.markdown("#### Investment by Business Type")
            st.bar_chart(pd.Series(np.random.rand(10), index=[f"Type {i}" for i in range(10)]))

import datetime
import streamlit as st

def render_risk_and_performance():
    # --- Centered Title ---
    st.markdown("<h2 style='text-align: center;'>Risk & Performance</h2>", unsafe_allow_html=True)

    # --- Date Filters ---
    inception_date = datetime.date(2020, 1, 1)
    today = datetime.date.today()

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=inception_date, key="risk_start")
    with col2:
        end_date = st.date_input("End Date", value=today, key="risk_end")

    # --- Metrics with Top Padding ---
    metrics = [
        ("Annualized Return", "12.4%"),
        ("Annualized Volatility", "8.9%"),
        ("Sharpe Ratio", "1.39"),
        ("Sortino Ratio", "2.01"),
        ("Max Drawdown", "-5.3%"),
        ("Calmar Ratio", "2.34"),
        ("Alpha", "1.8%"),
        ("Beta", "0.87"),
        ("Tracking Error", "2.1%"),
        ("Information Ratio", "0.87")
    ]

    for i in range(0, len(metrics), 5):
        if i > 1:
            st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)

        cols = st.columns(5)
        for col, (label, value) in zip(cols, metrics[i:i + 5]):
            col.markdown(f"""
                    <div style="
                        background-color: #f0f2f6;
                        border-radius: 12px;
                        padding: 1rem;
                        text-align: center;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
                    ">
                        <div style="font-size: 1.8rem; font-weight: 600; color: #333;">{value}</div>
                        <div style="font-size: 0.9rem; color: #666;">{label}</div>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # --- Side-by-side Charts: Rolling + Risk Factors ---
    st.markdown("### Risk Diagnostics")
    left, right = st.columns(2)

    # Rolling Risk Metric
    with left:
        rolling_metrics = {
            "Beta": pd.Series(np.random.uniform(0.7, 1.2, 100)),
            "Tracking Error": pd.Series(np.random.uniform(0.01, 0.05, 100)),
            "Excess Return": pd.Series(np.random.randn(100) / 100),
            "Information Ratio": pd.Series(np.random.uniform(0.2, 1.0, 100)),
            "Drawdown": pd.Series(np.random.uniform(-0.15, 0, 100)),
        }
        selected_metric = st.selectbox("Rolling Metric", list(rolling_metrics.keys()))
        st.line_chart(rolling_metrics[selected_metric].reset_index(drop=True))

    # Risk Factor Contribution
    with right:
        st.markdown("**Risk Contribution by Factor**")
        factors = ["Market", "Sector", "FX", "Rates", "Residual"]
        contributions = np.random.rand(5)
        st.plotly_chart(
            px.bar(x=factors, y=contributions, title="", labels={"x": "Factor", "y": "Contribution"}),
            use_container_width=True
        )