import numpy as np
import pandas as pd
from scipy.stats import linregress

class PerformanceStats:
    def __init__(self, strategy_returns, benchmark_returns, strat_equity_curve, bmk_equity_curve, trades, positions):
        self.strategy_returns = pd.Series(strategy_returns)
        self.benchmark_returns = pd.Series(benchmark_returns)
        self.strat_equity_curve = pd.Series(strat_equity_curve)
        self.bmk_equity_curve = pd.Series(bmk_equity_curve)
        self.trades = pd.DataFrame(trades)
        self.positions = pd.DataFrame(positions)
        self._calculate_performance()
        self._calculate_rolling_stats()
        self._calculate_exposures()
        self._calculate_attribution()
        self._summarize_trades()

    # --- Performance Metrics ---
    def _calculate_performance(self):
        rets = self.strategy_returns
        benchmark = self.benchmark_returns

        self.annualized_return = np.power(1 + rets.mean(), 252) - 1
        self.volatility = rets.std() * np.sqrt(252)
        self.sharpe = self.annualized_return / self.volatility
        self.sortino = self.annualized_return / (rets[rets < 0].std() * np.sqrt(252))
        self.max_drawdown = (self.strat_equity_curve / self.strat_equity_curve.cummax() - 1).min()
        self.calmar = self.annualized_return / abs(self.max_drawdown)

        self.alpha, self.beta = self._calc_alpha_beta(rets, benchmark)
        self.tracking_error = (rets - benchmark).std() * np.sqrt(252)
        self.information_ratio = (rets - benchmark).mean() / (rets - benchmark).std()

    def _calc_alpha_beta(self, strat, bench):
        slope, intercept, _, _, _ = linregress(bench, strat)
        return intercept * 252, slope

    # --- Rolling Metrics ---
    def _calculate_rolling_stats(self, window=21):
        self.rolling_vol = self.strategy_returns.rolling(window).std() * np.sqrt(252)
        self.rolling_sharpe = self.strategy_returns.rolling(window).mean() / self.strategy_returns.rolling(window).std()
        self.rolling_beta = self.benchmark_returns.rolling(window).corr(self.strategy_returns)
        self.rolling_te = (self.strategy_returns - self.benchmark_returns).rolling(window).std()

    # --- Exposure & Leverage ---
    def _calculate_exposures(self):
        if "sector" in self.positions.columns:
            self.sector_exposure = self.positions.groupby("sector")["weight"].mean()
        if "region" in self.positions.columns:
            self.geo_exposure = self.positions.groupby("region")["weight"].mean()
        if "asset_class" in self.positions.columns:
            self.asset_class_exposure = self.positions.groupby("asset_class")["weight"].mean()
        if "currency" in self.positions.columns:
            self.currency_exposure = self.positions.groupby("currency")["weight"].mean()

        self.net_exposure = self.positions.groupby("date")["weight"].sum()
        self.gross_exposure = self.positions.groupby("date")["weight"].apply(lambda w: np.abs(w).sum())
        self.leverage = self.positions.groupby("date")["leverage"].mean()

    # --- Attribution ---
    def _calculate_attribution(self):
        if "strategy" in self.trades.columns:
            self.strategy_contributions = self.trades.groupby("strategy")["pnl"].sum()

        if "signal" in self.trades.columns:
            self.signal_contributions = self.trades.groupby("signal")["pnl"].sum()

        # Heatmap: signals vs. average P&L per trade
        self.signal_heatmap = self.trades.pivot_table(index="signal", columns="instrument", values="pnl", aggfunc="mean").fillna(0)

        # Brinson placeholder (actual implementation depends on benchmark weights & returns)
        self.brinson_attribution = pd.Series({
            "Allocation Effect": 0.8,
            "Selection Effect": 1.2,
            "Interaction Effect": -0.1
        })

    # --- Trade Summary ---
    def _summarize_trades(self):
        df = self.trades
        self.total_trades = len(df)
        self.win_rate = (df["pnl"] > 0).mean()
        self.avg_return = df["pnl"].mean()
        self.median_return = df["pnl"].median()
        self.holding_period = (pd.to_datetime(df["exit_date"]) - pd.to_datetime(df["entry_date"])).dt.days.mean()
        self.largest_gain = df["pnl"].max()
        self.largest_loss = df["pnl"].min()

        self.trade_log = df.sort_values("exit_date", ascending=False)