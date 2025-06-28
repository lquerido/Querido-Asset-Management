import numpy as np
import pandas as pd

class PerformanceStats:
    def __init__(self, returns_df: pd.DataFrame, trades: pd.DataFrame, positions: pd.DataFrame):
        self.df = returns_df.copy()
        if "Date" in self.df.columns:
            self.df = self.df.set_index("Date")
        self.strategy_returns = self.df["strategy"]
        self.benchmark_returns = self.df["benchmark"]
        self.trades = trades.copy()
        self.positions = positions.copy()

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
        trades = self.trades.copy()
        positions = self.positions.copy()

        # --- Holding period (from positions) ---
        holding_periods = []
        positions.sort_values(["Ticker", "Date"], inplace=True)

        for ticker, group in positions.groupby("Ticker"):
            group = group.reset_index(drop=True)
            in_position = False
            start_date = None

            for i in range(len(group)):
                weight = group.loc[i, "Weight"]
                date = group.loc[i, "Date"]

                if not in_position and abs(weight) > 1e-4:
                    in_position = True
                    start_date = date
                elif in_position and abs(weight) <= 1e-4:
                    end_date = date
                    holding_periods.append((ticker, (end_date - start_date).days))
                    in_position = False

            # Still in position at end of sample
            if in_position:
                end_date = group["Date"].iloc[-1]
                holding_periods.append((ticker, (end_date - start_date).days))

        holding_df = pd.DataFrame(holding_periods, columns=["Ticker", "HoldingPeriod"])
        self.holding_period_avg = holding_df["HoldingPeriod"].mean() if not holding_df.empty else np.nan

        # --- Turnover (from trades) ---
        trades["Notional"] = trades["Quantity"] * trades["Execution Price"]
        total_notional = trades["Notional"].sum()
        avg_mv = positions.groupby("Date")["Market Value"].sum().mean()
        self.turnover = total_notional / avg_mv if avg_mv and avg_mv != 0 else np.nan

        # --- Win rate, avg/median pnl ---
        # Approximate PnL: positive for sells where execution price > signal price
        trades["SignedPnL"] = np.where(
            trades["Side"] == "BUY",
            -1 * (trades["Execution Price"] - trades["Signal Price"]) * trades["Quantity"],
            (trades["Execution Price"] - trades["Signal Price"]) * trades["Quantity"]
        )

        self.win_rate = (trades["SignedPnL"] > 0).mean() if not trades.empty else np.nan
        self.avg_pnl = trades["SignedPnL"].mean() if not trades.empty else np.nan
        self.median_pnl = trades["SignedPnL"].median() if not trades.empty else np.nan

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
