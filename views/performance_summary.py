import streamlit as st
import pandas as pd
import plotly.express as px

def render(subview):
    if subview == "Performance Analytics":
        st.header("Composite Portfolio Performance")

        if "backtest_results" in st.session_state:
            results = st.session_state["backtest_results"]

            # Key Metrics
            st.subheader("Key Metrics")
            stats_df = pd.DataFrame(results["performance_stats"], index=["Value"]).T
            st.table(stats_df)

            # Equity Curves
            st.subheader("Equity Curves")
            equity_df = pd.DataFrame({
                "Strategy": results["strategy_equity"],
                "Benchmark": results["benchmark_equity"]
            })
            st.line_chart(equity_df)

            # Returns
            st.subheader("Returns")
            returns_df = pd.DataFrame({
                "Strategy Returns": results["strategy_returns"],
                "Benchmark Returns": results["benchmark_returns"]
            })
            st.line_chart(returns_df)

            # Returns Histogram
            st.subheader("Return Distribution (Strategy)")
            fig = px.histogram(results["strategy_returns"], nbins=50, title="Strategy Return Distribution")
            st.plotly_chart(fig, use_container_width=True)

            # Trade Log (Optional)
            st.subheader("Trade Log")
            st.dataframe(pd.DataFrame(results["trade_log"]))

            # Execution Log (Optional)
            with st.expander("Execution Log"):
                st.dataframe(pd.DataFrame(results["execution_log"]))

        else:
            st.info("Run a backtest first.")
