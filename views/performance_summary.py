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

def dummy_series(n=100, scale=1):
    dates = pd.date_range(end=pd.Timestamp.today(), periods=n)
    data = np.cumsum(np.random.randn(n) * scale)
    return pd.Series(data, index=dates)


def render_summary():
    st.markdown("## Portfolio Dashboard")

    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Annualized Return", "12.4%")
        col2.metric("Volatility", "8.9%")
        col3.metric("Sharpe Ratio", "1.39")
        col4.metric("Sortino Ratio", "2.01")

        col5, col6, col7 = st.columns(3)
        col5.metric("Max Drawdown", "-5.3%")
        col6.metric("Calmar Ratio", "2.34")
        col7.metric("Information Ratio", "0.87")

    st.markdown("---")

    with st.container():
        st.markdown("### Equity Curve")
        st.line_chart(dummy_series())

# st.set_page_config(layout="wide")  # ✅ makes use of full browser width
#
# # Optional: extra styling tweaks
# st.markdown("""
#     <style>
#         .main .block-container {
#             padding-top: 1rem;
#             padding-bottom: 0rem;
#             padding-left: 2rem;
#             padding-right: 2rem;
#             max-width: 100% !important;
#         }
#     </style>
# """, unsafe_allow_html=True)



def render_summary():
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

    # # --- Chart Row 2 ---
    # with st.container():
    #     col = st.columns(1)[0]
    #     st.markdown("#### Ratings by Region")
    #     st.pyplot(px.pie(
    #         names=["North", "East", "West", "South"],
    #         values=[400, 300, 200, 100],
    #         title="Regions by Ratings"
    #     ).show())