import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pathlib import Path
import seaborn as sns

from backtest import (
    PriceData,
    MacroeconomicStrategy,
    TransactionCostModel,
    BacktestEngine,
    PerformanceStats,
    CompositeStrategy
)

# Cache price data so it's not downloaded every time
@st.cache_data
def get_price_data():
    return PriceData("SPY", "2010-01-01", "2024-12-31").data

def calculate_rolling_metrics(returns, benchmark_returns):
    excess_returns = returns - benchmark_returns
    
    # Rolling returns calculations
    rolling_periods = {
        '1Y': 252,
        '3Y': 252 * 3,
        '5Y': 252 * 5
    }
    
    metrics_df = pd.DataFrame(index=returns.index)
    
    for period_name, period in rolling_periods.items():
        metrics_df[f'Excess Returns {period_name}'] = excess_returns.rolling(period).mean() * 252
        metrics_df[f'Tracking Error {period_name}'] = excess_returns.rolling(period).std() * np.sqrt(252)
        metrics_df[f'Information Ratio {period_name}'] = (
            metrics_df[f'Excess Returns {period_name}'] / 
            metrics_df[f'Tracking Error {period_name}']
        )
    
    # Rolling beta (1Y)
    rolling_cov = returns.rolling(252).cov(benchmark_returns)
    rolling_var = benchmark_returns.rolling(252).var()
    metrics_df['Beta 1Y'] = rolling_cov / rolling_var
    
    return metrics_df

def plot_cumulative_returns(strategy_equity, benchmark_equity):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=strategy_equity.index, 
        y=strategy_equity/strategy_equity.iloc[0], 
        name='Strategy',
        line=dict(color='#00ff00', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=benchmark_equity.index, 
        y=benchmark_equity/benchmark_equity.iloc[0], 
        name='Benchmark',
        line=dict(color='#808080', width=2, dash='dash')
    ))
    fig.update_layout(
        title='Cumulative Returns',
        yaxis_title='Growth of $1',
        xaxis_title='Date',
        template='plotly_dark',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        height=400
    )
    return fig

def plot_excess_returns_dd(returns, benchmark_returns):
    excess_returns = returns - benchmark_returns
    cumulative_excess = (1 + excess_returns).cumprod()
    excess_dd = cumulative_excess / cumulative_excess.cummax() - 1
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=excess_dd.index,
        y=excess_dd,
        fill='tozeroy',
        name='Excess Return Drawdown',
        line=dict(color='#ff0000')
    ))
    fig.update_layout(
        title='Excess Return Drawdowns',
        yaxis_title='Drawdown (%)',
        xaxis_title='Date',
        template='plotly_white',
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        height=250,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    return fig

def plot_rolling_metrics(rolling_metrics):
    # Returns tab
    fig_returns = go.Figure()
    for period in ['1Y', '3Y', '5Y']:
        fig_returns.add_trace(go.Scatter(
            x=rolling_metrics.index,
            y=rolling_metrics[f'Excess Returns {period}'],
            name=f'{period}',
            line=dict(width=2)
        ))
    fig_returns.update_layout(
        title='Rolling Excess Returns',
        yaxis_title='Excess Return (ann.)',
        template='plotly_dark',
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=True,
        legend_title_text='Period'
    )
    # Risk tab
    fig_risk = go.Figure()
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    for i, period in enumerate(['1Y', '3Y', '5Y']):
        fig_risk.add_trace(go.Scatter(
            x=rolling_metrics.index,
            y=rolling_metrics[f'Tracking Error {period}'],
            name=f'{period}',
            line=dict(color=colors[i], width=2)
        ))
    fig_risk.add_trace(go.Scatter(
        x=rolling_metrics.index,
        y=rolling_metrics['Beta 1Y'],
        name='Beta (1Y)',
        line=dict(color=colors[3], width=2)
    ))
    fig_risk.update_layout(
        title='Rolling Risk Metrics',
        template='plotly_dark',
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=True,
        legend_title_text='Period'
    )
    # Information Ratio tab
    fig_ir = go.Figure()
    for i, period in enumerate(['1Y', '3Y', '5Y']):
        fig_ir.add_trace(go.Scatter(
            x=rolling_metrics.index,
            y=rolling_metrics[f'Information Ratio {period}'],
            name=f'{period}',
            line=dict(color=colors[i], width=2)
        ))
    fig_ir.update_layout(
        title='Rolling Information Ratio',
        template='plotly_white',
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=True,
        legend_title_text='Period',
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    return fig_returns, fig_risk, fig_ir
    
# Page setup
st.set_page_config(
    page_title="Querido Asset Management",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stApp {
        background-color: #0e1117;
    }
    .st-emotion-cache-18ni7ap {
        background-color: #0e1117;
    }
    .st-emotion-cache-1d3w5wq {
        width: 100%;
        padding: 3rem 1rem 1rem;
        max-width: 100%;
    }
    .stPlotlyChart {
        background-color: #262730;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    div[data-testid="stDataFrame"] {
        background-color: #262730;
        padding: 1rem;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    div[data-testid="stVerticalBlock"] > div {
        background-color: #262730;
        padding: 1rem;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .element-container {
        background-color: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)
# Sidebar navigation
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
    "Portfolio Updates",
    "About"
]
selection = st.sidebar.radio("Go to", tabs)

# --- Performance Summary ---
if selection == "Performance Summary":
    st.title("Performance Summary")
    
    # Get price data and run backtest
    prices = get_price_data()
    benchmark_prices = prices["Price"]
    
    # Create composite strategy
    tickers = ["SPY"]
    start_date = "2010-01-01"
    end_date = "2024-12-31"
    s1 = MacroeconomicStrategy("UNRATE", 5.0, tickers, start_date, end_date)
    s2 = MacroeconomicStrategy("CPIAUCSL", 250.0, tickers, start_date, end_date)
    s3 = MacroeconomicStrategy("GDP", 20000.0, tickers, start_date, end_date)
    strategy = CompositeStrategy([s1, s2, s3], [1/3, 1/3, 1/3])
    
    cost_model = TransactionCostModel()
    engine = BacktestEngine(benchmark_prices, strategy, cost_model)
    equity_curve, returns = engine.run()
    
    # Calculate benchmark returns
    benchmark_returns = benchmark_prices.pct_change()
    benchmark_equity = (1 + benchmark_returns).cumprod() * 100000
    
    # Calculate rolling metrics
    rolling_metrics = calculate_rolling_metrics(returns, benchmark_returns)
    # Layout
    col1, col2 = st.columns([7, 3])
    
    with col1:
        # Main performance chart
        st.plotly_chart(plot_cumulative_returns(equity_curve, benchmark_equity), use_container_width=True)
        
        # Excess return drawdowns
        st.plotly_chart(plot_excess_returns_dd(returns, benchmark_returns), use_container_width=True)
        
        # Rolling metrics tabs
        tab1, tab2, tab3 = st.tabs(['Returns', 'Risk', 'Risk-Adjusted'])
        fig_returns, fig_risk, fig_ir = plot_rolling_metrics(rolling_metrics)
        
        with tab1:
            st.plotly_chart(fig_returns, use_container_width=True)
        with tab2:
            st.plotly_chart(fig_risk, use_container_width=True)
        with tab3:
            st.plotly_chart(fig_ir, use_container_width=True)
    with col2:
        # Performance statistics
        st.subheader("Summary Statistics")
        stats = PerformanceStats(equity_curve, returns, benchmark_returns).compute()
        stats_df = pd.DataFrame(stats, index=["Metrics"]).T
        styled_stats = stats_df.style.format("{:.2%}")
        st.dataframe(styled_stats, use_container_width=True)
        
        # Latest metrics
        st.subheader("Latest Rolling Metrics")
        latest_metrics = rolling_metrics.iloc[-1].round(3)
        metrics_df = pd.DataFrame(latest_metrics).T
        st.dataframe(metrics_df, use_container_width=True)
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
    st.markdown(Path("docs/investment_philosophy.md").read_text())
elif selection == "Research & Commentary":
    st.title("📰 Research & Market Commentary")
    st.markdown(Path("docs/research.md").read_text())
elif selection == "Portfolio Updates":
    st.title("📈 Portfolio Updates")
    st.markdown(Path("docs/portfolio_updates.md").read_text())
elif selection == "About":
    st.title("👤 About")
    st.markdown(Path("docs/about.md").read_text())
