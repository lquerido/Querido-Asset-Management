import pandas as pd
import numpy as np
from pandas_datareader import data as web
import datetime
import yfinance as yf
from datasets.GetSeries import GetSeries
from strategies.signal_generation.MomentumStrategy import MomentumStrategy
from strategies.signal_generation.MeanReversionStrategy import MeanReversionStrategy
from strategies.allocations.VolatilityScaledAllocator import VolatilityScaledAllocator
from strategies.StrategyEnsemble import StrategyEnsemble
from strategies.InitialiseStrategy import InitialiseStrategy
from strategies.rebalancing.NaiveFullRebalancer import NaiveFullRebalancer


class TransactionCostModel:
    def __init__(self, slippage=0.0005, trading_fee=0.001):
        self.slippage = slippage
        self.trading_fee = trading_fee

    def apply_costs(self, positions: pd.Series) -> pd.Series:
        trades = positions.diff().abs().fillna(0)
        return trades * (self.slippage + self.trading_fee)

class BacktestEngine:
    def __init__(self, tickers, strategy, cost_model, start_date, end_date, rebalancer=NaiveFullRebalancer, initial_cash=100000, slippage=0.001, commission=0.0005):
        self.tickers = tickers
        self.strategy = strategy
        self.cost_model = cost_model
        self.start_date = start_date
        self.end_date = end_date
        self.balance = initial_cash
        self.rebalancer = rebalancer
        self.weights = {}
        self.slippage = slippage
        self.commission = commission

    def get_security_weights(self):
        """
        Returns the current open positions based on the strategy signals.
        """
        return self.weights

    def get_rebalanced_weights(self, current_weights, target_weights):
        """
        Rebalances the portfolio to match the target weights.
        """
        trades, rebalanced_weights = self.rebalancer().rebalance(current_weights, target_weights)
        return trades, rebalanced_weights

    def fetch_series(self, tickers, start, end):
        """
        Fetches historical price data for the given tickers and date range.
        """
        return GetSeries(ticker=tickers, start=start, end=end)

    def update_holdings_with_execution(self, trades: dict, price_row: pd.Series) -> dict:
        for ticker, target_trade in trades.items():
            if ticker == "CASH":
                continue

            price = price_row[ticker]
            direction = np.sign(target_trade)
            slippage_factor = 1 + self.slippage * direction
            exec_price = price * slippage_factor
            trade_value = abs(target_trade) * exec_price
            commission = trade_value * self.commission

            if direction > 0 and self.cash >= trade_value + commission:     # Todo: Fix cash allocation
                # Buy
                self.cash -= (trade_value + commission)
                self.holdings[ticker] = self.holdings.get(ticker, 0) + target_trade
            elif direction < 0 and self.holdings.get(ticker, 0) >= abs(target_trade):
                # Sell
                self.cash += trade_value - commission
                self.holdings[ticker] = self.holdings.get(ticker, 0) + target_trade  # Note: target_trade is negative

        return self.holdings

    def run(self):
        prices = self.fetch_series(self.tickers, self.start_date, self.end_date).fetch_prices()
        returns = self.fetch_series(self.tickers, self.start_date, self.end_date).fetch_returns()
        trade_log = []
        for date in prices.index:
            # Generate positions using the strategy (using data to the current date)
            for strat, strat_params in self.strategy.capital_allocation.items():
                strat_instance, capital_fraction = strat_params
                strat_instance.end = date
            current_weights = self.get_security_weights()
            target_weights = self.strategy.aggregate_allocations()
            trades, rebalanced_weights = self.get_rebalanced_weights(current_weights, target_weights)
            executed_weights = self.update_holdings_with_execution(trades, prices.loc[date])

            for trade in trades:
                if trade != 0:
                    self._log_trade(date, trade, 'BUY' if trade > 0 else 'SELL', abs(trade), prices.loc[date, trade], prices.loc[date, trade], strat)
            self.weights.update(rebalanced_weights)
            print('Done')


    def _log_trade(self, date, ticker, side, qty, signal_price, execution_price, signal):
        self.trade_log.append({
            "Date": date,
            "Ticker": ticker,
            "Side": side,
            "Quantity": qty,
            "Signal Price": round(signal_price, 2),
            "Execution Price": round(execution_price, 2),
            "Signal": signal
        })

    def _log_account(self, date, prices):
        holdings_value = sum(qty * prices[ticker] for ticker, qty in self.holdings.items() if ticker in prices)
        total_value = self.cash + holdings_value
        gross_exposure = sum(abs(qty * prices[ticker]) for ticker, qty in self.holdings.items() if ticker in prices)
        net_exposure = sum(qty * prices[ticker] for ticker, qty in self.holdings.items() if ticker in prices)

        self.account_history.append({
            "Date": date,
            "Cash": round(self.cash, 2),
            "Holdings Value": round(holdings_value, 2),
            "Total Value": round(total_value, 2),
            "Gross Exposure": round(gross_exposure, 2),
            "Net Exposure": round(net_exposure, 2)
        })



def main(tickers, composite, benchmark_ticker, start_date, end_date, slippage=0.001, commission=0.0005):
    cost_model = TransactionCostModel()
    engine = BacktestEngine(tickers, composite, cost_model, start_date, end_date, slippage=slippage, commission=commission)
    equity, returns = engine.run()
    #
    # # Benchmark = SPY
    # benchmark_ticker = "SPY"
    # spy = yf.download(benchmark_ticker, start=start_date, end=end_date)["Close"]
    # benchmark_returns = spy.pct_change()[benchmark_ticker].reindex(returns.index).dropna()
    #
    # stats = PerformanceStats(equity, returns, benchmark_returns).compute()
    # print(stats)


if __name__ == '__main__':
    tickers = ["AAPL", "MSFT", "GOOG", "TSLA"]

    mean_rev = InitialiseStrategy(
        strategy_cls=MeanReversionStrategy,
        allocator_cls=VolatilityScaledAllocator,
        tickers=tickers,
        start="2020-01-01",
        end="2024-12-31",
        strategy_kwargs={"lookback": 20, "bound": 2}
    )

    momentum = InitialiseStrategy(
        strategy_cls=MomentumStrategy,
        allocator_cls=VolatilityScaledAllocator,
        tickers=tickers,
        start="2020-01-01",
        end="2024-12-31",
        strategy_kwargs={"lookback": 20, "threshold": 0.02}
    )

    capital_allocation = {
        "mean_reversion": (mean_rev, 0.5),
        "momentum": (momentum, 0.5)
    }

    ensemble = StrategyEnsemble(capital_allocation)
    main(
        tickers,
        ensemble,
        benchmark_ticker="SPY",
        start_date="2020-01-01",
        end_date="2024-12-31",
        slippage=0.001,
        commission=0.0005
    )
    print('Ensemble Weights:', ensemble.aggregate_allocations())