import numpy as np
import pandas as pd

class PerformanceStats:
    def __init__(self, returns_df: pd.DataFrame, trades: pd.DataFrame, positions: pd.DataFrame):
        self.df = returns_df.copy()
        if "date" in self.df.columns:
            self.df = self.df.set_index("date")
        self.strategy_returns = self.df["strategy"]
        self.benchmark_returns = self.df["benchmark"]
        self.trades = trades.copy()
        self.positions = positions.copy()       # Todo: Need tickers? And cash should be a line item within the holdings

        self._calculate_performance()
        self._calculate_rolling()
        self._calculate_trade_summary()

    def _calculate_performance(self):
        r, b = self.strategy_returns, self.benchmark_returns
        excess = r - b

        self.total_return = (1 + r).prod() - 1
        self.excess_return = (1 + excess).prod() - 1
        self.annualized_return = (1 + r.mean()) ** 252 - 1

        self.volatility = r.std() * np.sqrt(252)
        self.tracking_error = excess.std() * np.sqrt(252)

        self.sharpe = r.mean() / r.std() * np.sqrt(252) if r.std() > 0 else np.nan
        self.info_ratio = excess.mean() / excess.std() if excess.std() > 0 else np.nan
        self.beta = r.cov(b) / b.var() if b.var() > 0 else np.nan

        cum = (1 + r).cumprod()
        self.max_drawdown = ((cum / cum.cummax()) - 1).min()

        self.up_capture = r[b > 0].mean() / b[b > 0].mean() if not b[b > 0].empty else np.nan
        self.down_capture = r[b < 0].mean() / b[b < 0].mean() if not b[b < 0].empty else np.nan

    def _calculate_rolling(self, window=21):
        self.rolling_sharpe = self.strategy_returns.rolling(window).mean() / self.strategy_returns.rolling(window).std()
        excess = self.strategy_returns - self.benchmark_returns
        self.rolling_ir = excess.rolling(window).mean() / excess.rolling(window).std()
        self.rolling_volatility = self.strategy_returns.rolling(window).std() * np.sqrt(252)

    def _calculate_trade_summary(self):
        df = self.trades.copy()
        df["entry_date"] = pd.to_datetime(df["entry_date"])     # Todo: Not tracking entry and exit date
        df["exit_date"] = pd.to_datetime(df["exit_date"])

        total_notional = df["notional"].sum()
        avg_mv = self.positions["market_value"].abs().mean() if not self.positions.empty else np.nan
        self.turnover = total_notional / avg_mv if avg_mv != 0 else np.nan

        self.win_rate = (df["pnl"] > 0).mean() if not df.empty else np.nan
        self.avg_pnl = df["pnl"].mean() if not df.empty else np.nan
        self.median_pnl = df["pnl"].median() if not df.empty else np.nan
        self.holding_period_avg = (df["exit_date"] - df["entry_date"]).dt.days.mean() if not df.empty else np.nan

    def to_dict(self):
        return {
            "Total Return": self.total_return,
            "Excess Return": self.excess_return,
            "Annualized Return": self.annualized_return,
            "Volatility": self.volatility,
            "Tracking Error": self.tracking_error,
            "Sharpe Ratio": self.sharpe,
            "Information Ratio": self.info_ratio,
            "Beta": self.beta,
            "Max Drawdown": self.max_drawdown,
            "Up Capture": self.up_capture,
            "Down Capture": self.down_capture,
            "Turnover": self.turnover,
            "Win Rate": self.win_rate,
            "Avg PnL": self.avg_pnl,
            "Median PnL": self.median_pnl,
            "Holding Period": self.holding_period_avg,
        }
