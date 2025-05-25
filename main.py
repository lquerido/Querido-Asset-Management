import pandas as pd
import numpy as np

class SignalStrategy:
    def generate_signals(self, prices: pd.Series) -> pd.Series:
        return pd.Series(1, index=prices.index, name="Signal")  # always long

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
        positions = signals.copy()
        gross_returns = positions.shift(1).fillna(0) * returns
        cost_penalty = self.cost_model.apply_costs(positions)
        net_returns = gross_returns - cost_penalty
        equity_curve = (1 + net_returns).cumprod() * self.initial_cash
        return equity_curve, net_returns

class PerformanceStats:
    def __init__(self, equity_curve, returns):
        self.equity_curve = equity_curve
        self.returns = returns

    def compute(self):
        ann_return = (self.equity_curve.iloc[-1] / self.equity_curve.iloc[0]) ** (252 / len(self.equity_curve)) - 1
        vol = self.returns.std() * np.sqrt(252)
        sharpe = ann_return / vol if vol > 0 else np.nan
        drawdown = (self.equity_curve / self.equity_curve.cummax() - 1).min()
        return {
            "Annualized Return": ann_return,
            "Annualized Volatility": vol,
            "Sharpe Ratio": sharpe,
            "Max Drawdown": drawdown
        }


if __name__ == 'main':
    strategy = SignalStrategy()
    cost_model = TransactionCostModel()
    engine = BacktestEngine(prices, strategy, cost_model)
    equity, rets = engine.run()

    stats = PerformanceStats(equity, rets).compute()
    print(stats)
