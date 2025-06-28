# app_state.py
import streamlit as st
from simulation.StrategyExecution import main as run_backtest
from strategies.InitialiseStrategy import InitialiseStrategy
from strategies.StrategyEnsemble import StrategyEnsemble
from strategies.signal_generation.MomentumStrategy import MomentumStrategy
from strategies.signal_generation.MeanReversionStrategy import MeanReversionStrategy
from strategies.signal_generation.BuyAndHoldStrategy import BuyAndHoldStrategy
from strategies.allocations.VolatilityScaledAllocator import VolatilityScaledAllocator
from strategies.allocations.EqualWeightAllocator import EqualWeightAllocator
from datasets.GetSeries import GetSeries
from utils.helper_functions import build_fund_registry


@st.cache_data(show_spinner=True)
def get_performance_stats(fund, start_date, end_date):
    tickers = ["AAPL", "MSFT", "GOOG", "TSLA"]
    prices = GetSeries(ticker=tickers, start=start_date, end=end_date).fetch_prices()

    fund_registry = build_fund_registry(start_date, end_date, tickers)
    strat = fund_registry[fund]

    benchmark = InitialiseStrategy(
        strategy_cls=MeanReversionStrategy,
        allocator_cls=EqualWeightAllocator,
        tickers=["SPY"],
        start=start_date,
        end=end_date,
        strategy_kwargs={"lookback": 20, "bound": 1.5},
        allocator_kwargs={}
    )

    from simulation.StrategyExecution import main as run_backtest
    return run_backtest(
        tickers=tickers,
        strat=strat,
        benchmark_ticker="SPY",
        benchmark_strat=benchmark,
        start_date=start_date,
        end_date=end_date,
        slippage=0.001,
        commission=0.0005
    )
