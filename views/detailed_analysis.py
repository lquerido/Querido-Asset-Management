import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def render(subview):
    st.title("Detailed Investment Performance Analysis")

    if subview == "Trade-by-Trade Analysis":
        st.subheader("Trade-by-Trade Breakdown")
        data = pd.DataFrame({
            "Security": ["AAPL", "GOOGL", "TSLA", "MSFT"],
            "Entry Date": ["2024-01-15", "2024-02-10", "2024-03-01", "2024-04-05"],
            "Exit Date": ["2024-02-15", "2024-03-10", "2024-03-30", "2024-05-01"],
            "PnL": [1200, -800, 600, 900],
            "Holding Period": [30, 29, 29, 26]
        })
        st.dataframe(data)

    elif subview == "Time-Weighted Returns":
        st.subheader("Cumulative Return vs Benchmark")
        dates = pd.date_range(start="2024-01-01", periods=100)
        portfolio = np.cumprod(1 + np.random.normal(0.0005, 0.01, size=100))
        benchmark = np.cumprod(1 + np.random.normal(0.0004, 0.009, size=100))
        df = pd.DataFrame({"Date": dates, "Portfolio": portfolio, "Benchmark": benchmark})
        st.line_chart(df.set_index("Date"))

    elif subview == "Portfolio Composition":
        st.subheader("Current Weights")
        weights = pd.Series({
            "Tech": 0.35,
            "Healthcare": 0.20,
            "Finance": 0.15,
            "Energy": 0.10,
            "Industrials": 0.10,
            "Other": 0.10
        })
        st.bar_chart(weights)

    elif subview == "Portfolio Risk":
        st.subheader("Risk Metrics")
        st.metric("30-Day Volatility", "12.5%")
        st.metric("Max Drawdown", "-8.2%")
        st.metric("Beta vs Benchmark", "1.1")
        st.metric("Value-at-Risk (95%)", "-3.2%")

    elif subview == "Performance Factors":
        st.subheader("Factor Exposure Summary")
        factors = pd.DataFrame({
            "Factor": ["Momentum", "Value", "Size", "Volatility", "Quality"],
            "Exposure": [0.25, -0.10, 0.05, 0.15, 0.20]
        })
        st.dataframe(factors)
        st.metric("Turnover", "35%")
        st.metric("Win Rate", "62%")


def render_attribution():
    st.set_page_config(layout="wide")
    st.subheader("Performance Attribution")

    # Metric cards
    st.markdown("""
        <style>
            .metric-card {
                background-color: #f8f9fa;
                border-radius: 1rem;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                height: 100%;
            }
            .metric-number {
                font-size: 2rem;
                font-weight: bold;
                margin-bottom: 0.25rem;
            }
            .metric-label {
                font-size: 0.9rem;
                color: #6c757d;
            }
        </style>
    """, unsafe_allow_html=True)

    metrics = [
        {"label": "Total Attribution", "value": "+6.7%"},
        {"label": "Top Strategy", "value": "Momentum"},
        {"label": "Worst Strategy", "value": "Mean Reversion"},
    ]

    cols = st.columns(3)
    for i, metric in enumerate(metrics):
        with cols[i]:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-number">{metric['value']}</div>
                    <div class="metric-label">{metric['label']}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("#### Strategy Contributions")
    strategy_contrib = pd.DataFrame({
        "Strategy": ["Momentum", "Mean Reversion", "Buy & Hold"],
        "Contribution (%)": [4.2, -1.1, 3.6]
    })
    st.dataframe(strategy_contrib, use_container_width=True)

    chart_cols = st.columns(2)
    with chart_cols[0]:
        st.markdown("#### Sector Attribution")
        st.bar_chart(pd.Series(
            np.random.randn(5), index=[f"Sector {i+1}" for i in range(5)]
        ))

    with chart_cols[1]:
        st.markdown("#### Rolling Strategy Contribution")
        df = pd.DataFrame(
            np.cumsum(np.random.randn(100, 3), axis=0),
            columns=["Momentum", "Mean Reversion", "Buy & Hold"]
        )
        st.line_chart(df)
