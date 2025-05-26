import pandas as pd
import numpy as np
from pandas_datareader import data as web
import datetime
import yfinance as yf

class MacroeconomicStrategy:
    def __init__(self, indicator: str, threshold: float, tickers: list, start: str, end: str):
        self.indicator = indicator
        self.threshold = threshold
        self.tickers = tickers
        self.start = start
        self.end = end
        self.data = self.fetch_data()

    def fetch_data(self) -> pd.Series:
        start_dt = datetime.datetime.strptime(self.start, "%Y-%m-%d")
        end_dt = datetime.datetime.strptime(self.end, "%Y-%m-%d")
        data = web.DataReader(self.indicator, 'fred', start_dt, end_dt)
        return data[self.indicator]

    def generate_signals(self, prices: pd.DataFrame) -> pd.DataFrame:
        macro = self.data.reindex(prices.index, method='ffill')
        signal = (macro > self.threshold).astype(int)
        return pd.DataFrame(signal.values[:, None] * np.ones((len(prices), len(self.tickers))),
                            index=prices.index, columns=self.tickers)

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

class PerformanceStats:
    def __init__(self, equity_curve, returns, benchmark_returns, rf_rate=0.015):
        self.equity_curve = equity_curve
        self.returns = returns
        self.benchmark_returns = benchmark_returns
        self.rf_rate = rf_rate

    def compute(self):
        ann_return = (self.equity_curve.iloc[-1] / self.equity_curve.iloc[0]) ** (252 / len(self.equity_curve)) - 1
        vol = self.returns.std() * np.sqrt(252)
        sharpe = (ann_return - self.rf_rate) / vol if vol > 0 else np.nan
        drawdown = (self.equity_curve / self.equity_curve.cummax() - 1).min()
        tracking_error = np.std(self.returns - self.benchmark_returns) * np.sqrt(252)
        beta = np.cov(self.returns, self.benchmark_returns)[0, 1] / np.var(self.benchmark_returns)
        alpha = ann_return - self.rf_rate - beta * (self.benchmark_returns.mean() * 252 - self.rf_rate)
        upside = self.returns[self.benchmark_returns > 0].mean() / self.benchmark_returns[self.benchmark_returns > 0].mean()
        downside = self.returns[self.benchmark_returns < 0].mean() / self.benchmark_returns[self.benchmark_returns < 0].mean()

        return {
            "Annualized Return": ann_return,
            "Annualized Volatility": vol,
            "Sharpe Ratio": sharpe,
            "Max Drawdown": drawdown,
            "Tracking Error": tracking_error,
            "Beta": beta,
            "Alpha": alpha,
            "Upside Capture": upside,
            "Downside Capture": downside
        }

def main():
    tickers = ["AAPL", "MSFT", "GOOGL", "XOM", "JNJ"]
    start_date = "2020-01-01"
    end_date = "2024-12-31"

    price_data = yf.download(tickers, start=start_date, end=end_date)["Close"]

    # Define macro strategies over all tickers
    s1 = MacroeconomicStrategy("UNRATE", 5.0, tickers, start_date, end_date)
    s2 = MacroeconomicStrategy("CPIAUCSL", 250.0, tickers, start_date, end_date)
    s3 = MacroeconomicStrategy("GDP", 20000.0, tickers, start_date, end_date)
    strategies = [s1, s2, s3]
    weights = [1/3, 1/3, 1/3]

    composite = CompositeStrategy(strategies, weights)
    cost_model = TransactionCostModel()
    engine = BacktestEngine(price_data, composite, cost_model)
    equity, returns = engine.run()

    # Benchmark = SPY
    spy = yf.download("SPY", start=start_date, end=end_date)["Close"]
    benchmark_returns = spy.pct_change().reindex(returns.index).fillna(0)

    stats = PerformanceStats(equity, returns, benchmark_returns).compute()
    print(stats)

if __name__ == "__main__":
    main()