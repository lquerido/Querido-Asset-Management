import streamlit as st
import pandas as pd
import numpy as np

from stats.performance import PerformanceStats

def render(subview):
    if subview == "Performance Analytics":
        st.header("Composite Portfolio Performance")

        # Dummy returns for illustration
        composite_returns = pd.Series(np.random.randn(252) / 100)
        strategy_returns = {
            "Mean Reversion": pd.Series(np.random.randn(252) / 100),
            "Momentum": pd.Series(np.random.randn(252) / 100),
            "Macro Filter": pd.Series(np.random.randn(252) / 100)
        }
        bencmark_returns = pd.Series(np.random.randn(252) / 100)

        stats = PerformanceStats(composite_returns, strategy_returns, bencmark_returns)

        # Display Summary Table
        st.subheader("Key Metrics")
        st.table(stats.compute())

        # # Attribution Chart
        # attribution = stats.attribution()
        # if attribution is not None:
        #     st.subheader("Attribution by Strategy")
        #     st.bar_chart(attribution)
        # else:
        #     st.info("Attribution data not available.")
