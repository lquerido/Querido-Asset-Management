import pandas as pd
import numpy as np
from pandas_datareader import data as web
import datetime
import yfinance as yf
from datasets.GetSeries import GetPriceSeries
from strategies.MomentumStrategy import MomentumStrategy



class CompositeStrategy:
    def __init__(self, strategies, weights):
        self.strategies = strategies
        self.weights = weights

    def generate_signals(self, prices: pd.DataFrame) -> pd.DataFrame:
        signal_dfs = []
        for strategy, weight in zip(self.strategies, self.weights):
            signals = strategy.generate_signals(prices)
            signal_dfs.append(signals * weight)
        combined = sum(signal_dfs)
        row_sums = combined.sum(axis=1)
        normalized = combined.div(row_sums, axis=0).fillna(0)
        return normalized

class TransactionCostModel:
    def __init__(self, slippage=0.0005, trading_fee=0.001):
        self.slippage = slippage
        self.trading_fee = trading_fee

    def apply_costs(self, positions: pd.Series) -> pd.Series:
        trades = positions.diff().abs().fillna(0)
        return trades * (self.slippage + self.trading_fee)

class BacktestEngine:
    def __init__(self, prices, strategy, cost_model, initial_cash=100000):
        self.prices = prices
        self.strategy = strategy
        self.cost_model = cost_model
        self.initial_cash = initial_cash

    def run(self):
        signals = self.strategy.generate_signals(self.prices)
        returns = self.prices.pct_change().fillna(0)
        weights = signals.shift(1).fillna(0)
        portfolio_returns = (weights * returns).sum(axis=1)
        cost_penalty = self.cost_model.apply_costs(weights.sum(axis=1))
        net_returns = portfolio_returns - cost_penalty
        equity_curve = (1 + net_returns).cumprod() * self.initial_cash
        return equity_curve, net_returns



def main():
    tickers = ["AAPL", "MSFT", "GOOGL", "XOM", "JNJ"]
    start_date = "2020-01-01"
    end_date = "2024-12-31"

    price_data = yf.download(tickers, start=start_date, end=end_date)["Close"]

    # Define macro strategies over all tickers
    s1 = MomentumStrategy("UNRATE", 5.0, tickers, start_date, end_date)
    s2 = MomentumStrategy("CPIAUCSL", 250.0, tickers, start_date, end_date)
    strategies = [s1, s2]
    weights = [0.6, 0.4]

    composite = CompositeStrategy(strategies, weights)
    cost_model = TransactionCostModel()
    engine = BacktestEngine(price_data, composite, cost_model)
    equity, returns = engine.run()

    # Benchmark = SPY
    benchmark_ticker = "SPY"
    spy = yf.download(benchmark_ticker, start=start_date, end=end_date)["Close"]
    benchmark_returns = spy.pct_change()[benchmark_ticker].reindex(returns.index).fillna(0)

    from stats.performance import PerformanceStats

    stats = PerformanceStats(equity, returns, benchmark_returns).compute()
    print(stats)

if __name__ == "__main__":
    main()