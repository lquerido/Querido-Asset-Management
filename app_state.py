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

@st.cache_data(show_spinner=True)
def get_performance_stats():
    tickers = ["AAPL", "MSFT", "GOOG", "TSLA"]
    start = "2020-01-01"
    end = "2024-12-31"
    vol_data = GetSeries(ticker=tickers, start=start, end=end).fetch_volatility()

    mean_rev = InitialiseStrategy(
        strategy_cls=MeanReversionStrategy,
        allocator_cls=VolatilityScaledAllocator,
        tickers=tickers,
        start=start,
        end=end,
        strategy_kwargs={"lookback": 20, "bound": 2},
        allocator_kwargs={"vol_data": vol_data}
    )
    momentum = InitialiseStrategy(
        strategy_cls=MomentumStrategy,
        allocator_cls=VolatilityScaledAllocator,
        tickers=tickers,
        start=start,
        end=end,
        strategy_kwargs={"lookback": 20, "threshold": 0.02},
        allocator_kwargs={"vol_data": vol_data}
    )

    capital_allocation = {
        "mean_reversion": (mean_rev, 0.5),
        "momentum": (momentum, 0.5)
    }
    ensemble = StrategyEnsemble(capital_allocation)

    benchmark = InitialiseStrategy(
        strategy_cls=BuyAndHoldStrategy,
        allocator_cls=EqualWeightAllocator,
        tickers="SPY",
        start=start,
        end=end
    )

    return run_backtest(
        tickers=tickers,
        strat=ensemble,
        benchmark_ticker="SPY",
        benchmark_strat=benchmark,
        start_date=start,
        end_date=end,
        slippage=0.001,
        commission=0.0005
    )
