import numpy as np

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
        # beta = np.cov(self.returns, self.benchmark_returns)[0, 1] / np.var(self.benchmark_returns)
        # alpha = ann_return - self.rf_rate - beta * (self.benchmark_returns.mean() * 252 - self.rf_rate)
        upside = self.returns[self.benchmark_returns > 0].mean() / self.benchmark_returns[self.benchmark_returns > 0].mean()
        downside = self.returns[self.benchmark_returns < 0].mean() / self.benchmark_returns[self.benchmark_returns < 0].mean()

        return {
            "Annualized Return": ann_return,
            "Annualized Volatility": vol,
            "Sharpe Ratio": sharpe,
            "Max Drawdown": drawdown,
            "Tracking Error": tracking_error,
            # "Beta": beta,
            # "Alpha": alpha,
            "Upside Capture": upside,
            "Downside Capture": downside
        }