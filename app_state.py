import streamlit as st
from datasets.GetSeries import GetSeries
from simulation.StrategyExecution import main as run_backtest
from strategies.InitialiseStrategy import InitialiseStrategy
from strategies.signal_generation.BuyAndHoldStrategy import BuyAndHoldStrategy
from strategies.signal_generation.MeanReversionStrategy import MeanReversionStrategy
from strategies.allocations.EqualWeightAllocator import EqualWeightAllocator
from utils.helper_functions import build_fund_registry
from strategies.StrategyEnsemble import StrategyEnsemble

@st.cache_data(show_spinner=True)
def get_performance_stats(fund, start_date, end_date):
    fund_components = build_fund_registry(start_date, end_date)[fund]

    individual_stats = {}

    for name, (strat, weight) in fund_components.capital_allocation.items():
        tickers = strat.tickers if hasattr(strat, "tickers") else []  # get tickers from strat

        stats = run_backtest(       # Todo Merge this into the running of the main backtest
            tickers=tickers,
            strat=strat,
            benchmark_ticker="SPY",
            benchmark_strat=InitialiseStrategy(
                strategy_cls=MeanReversionStrategy,
                allocator_cls=EqualWeightAllocator,
                tickers=["SPY"],
                start=start_date,
                end=end_date,
                strategy_kwargs={"lookback": 20, "bound": 1.5},
                allocator_kwargs={}
            ),
            start_date=start_date,
            end_date=end_date,
            slippage=0.001,
            commission=0.0005
        )
        individual_stats[name] = stats

    # Composite strategy
    capital_allocation = {
        name: (strat, weight) for name, (strat, weight) in fund_components.capital_allocation.items()
    }
    all_tickers = sorted(set(
        t
        for strat, _ in fund_components.capital_allocation.values()
        for t in strat.tickers
    ))

    ensemble = StrategyEnsemble(capital_allocation)
    print('Ensemble Weights:', ensemble.aggregate_allocations())

    benchmark = InitialiseStrategy(
        strategy_cls=BuyAndHoldStrategy,
        allocator_cls=EqualWeightAllocator,
        tickers="SPY",
        start=start_date,
        end=end_date
    )
    composite_stats = run_backtest(
        all_tickers,        # Todo: Use the tickers from the underlying strategies
        ensemble,
        benchmark_ticker="SPY",
        benchmark_strat=benchmark,
        start_date=start_date,
        end_date=end_date,
        slippage=0.001,
        commission=0.0005
    )

    return {
        "composite": composite_stats,
        "strategies": individual_stats
    }
