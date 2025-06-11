import pandas as pd
from datasets.GetSeries import GetSeries
from strategies.signal_generation.MomentumStrategy import MomentumStrategy
from strategies.signal_generation.MeanReversionStrategy import MeanReversionStrategy
from strategies.signal_generation.BuyAndHoldStrategy import BuyAndHoldStrategy
from strategies.allocations.VolatilityScaledAllocator import VolatilityScaledAllocator
from strategies.allocations.EqualWeightAllocator import EqualWeightAllocator
from strategies.StrategyEnsemble import StrategyEnsemble
from strategies.InitialiseStrategy import InitialiseStrategy
from strategies.rebalancing.NaiveFullRebalancer import NaiveFullRebalancer
from stats.PerformanceStats import PerformanceStats


class TransactionCostModel:
    def __init__(self, slippage=0.0005, trading_fee=0.001):
        self.slippage = slippage
        self.trading_fee = trading_fee

    def apply_costs(self, positions: pd.Series) -> pd.Series:
        trades = positions.diff().abs().fillna(0)
        return trades * (self.slippage + self.trading_fee)

class BacktestEngine:
    def __init__(
        self,
        tickers,
        strategy,
        cost_model,
        start_date,
        end_date,
        rebalancer=NaiveFullRebalancer,
        cash_buffer=0.02,
        initial_cash=100000,
        slippage=0.001,
        commission=0.0005,
        benchmark_strat=None
    ):
        self.tickers = tickers
        self.strategy = self._wrap_if_single(strategy)
        self.benchmark_strategy = self._wrap_if_single(benchmark_strat) if benchmark_strat else None
        self.cost_model = cost_model
        self.start_date = start_date
        self.end_date = end_date
        self.cash = initial_cash
        self.rebalancer = rebalancer
        self.cash_buffer = cash_buffer
        self.holdings = {}  # {ticker: quantity}
        self.slippage = slippage
        self.commission = commission
        self.execution_log = []
        self.trade_log = []
        self.account_history = []

    def _wrap_if_single(self, strat):
        if strat is None:
            return None
        if hasattr(strat, "aggregate_allocations"):
            return strat  # Already a StrategyEnsemble
        return StrategyEnsemble({"wrapped_strategy": (strat, 1.0)})

    def get_rebalanced_weights(self, target_weights):
        """
        Rebalances the portfolio to match the target weights.
        """
        trades, rebalanced_weights = self.rebalancer().rebalance(self.holdings, target_weights)
        return trades, rebalanced_weights

    def fetch_series(self, tickers, start, end):
        """
        Fetches historical price data for the given tickers and date range.
        """
        return GetSeries(ticker=tickers, start=start, end=end)

    def portfolio_value(self, prices: pd.Series) -> float:
        equity = sum(
            qty * prices.get(ticker, 0) for ticker, qty in self.holdings.items()
        )
        return self.cash + equity

    def get_weights(self, prices: pd.Series) -> float:
        equity = sum(
            qty * prices.get(ticker, 0) for ticker, qty in self.holdings.items()
        )
        return self.cash + equity

    def _process_trades(self, trades: dict, prices: pd.Series, simulate: bool = False) -> bool | dict:
        temp_cash = self.cash
        temp_holdings = self.holdings.copy()
        usable_portfolio_val = self.portfolio_value(prices) * (1 - self.cash_buffer)  # Cash buffer to ensure liquidity and enough cash for trades
        portfolio_val = usable_portfolio_val
        executed_info = {}  # {ticker: {"qty": X, "price": Y}}

        # --- Execute sells first ---
        for ticker, trade_weight in trades.items():
            if trade_weight >= 0 or ticker == "CASH":
                continue
            trade_value = abs(trade_weight) * portfolio_val
            exec_price = prices[ticker] * (1 - self.slippage)
            commission = trade_value * self.commission
            # qty = int(trade_value // exec_price)
            qty = trade_value / exec_price

            if temp_holdings.get(ticker, 0) < qty:
                return False if simulate else None

            if not simulate:
                self.cash += trade_value - commission
                self.holdings[ticker] -= qty
            else:
                temp_cash += trade_value - commission
                temp_holdings[ticker] -= qty

            executed_info[ticker] = {"qty": qty, "price": exec_price}

        # --- Execute buys ---
        for ticker, trade_weight in trades.items():
            if trade_weight <= 0 or ticker == "CASH":
                continue
            trade_value = trade_weight * portfolio_val
            exec_price = prices[ticker] * (1 + self.slippage)
            commission = trade_value * self.commission
            total_cost = trade_value + commission
            # qty = int(trade_value // exec_price)
            qty = trade_value / exec_price

            if temp_cash < total_cost:
                print(f"Ticker: {ticker}: Cash shortfall: {temp_cash / total_cost}")
                return False if simulate else None

            if not simulate:
                self.cash -= total_cost
                self.holdings[ticker] = self.holdings.get(ticker, 0) + qty
            else:
                temp_cash -= total_cost
                temp_holdings[ticker] = temp_holdings.get(ticker, 0) + qty

            executed_info[ticker] = {"qty": qty, "price": exec_price}

        return True if simulate else executed_info


    def run(self):
        print('Running backtest...')
        prices = self.fetch_series(self.tickers, self.start_date, self.end_date).fetch_prices()
        # returns = self.fetch_series(self.tickers, self.start_date, self.end_date).fetch_returns()
        # trade_log = []
        for date in prices.index:
            # Generate positions using the strategy (using data to the current date)
            for strat, strat_params in self.strategy.capital_allocation.items():
                strat_instance, capital_fraction = strat_params
                strat_instance.end = date
            # Generate target positions
            target_weights = self.strategy.aggregate_allocations()
            trades, rebalanced_weights = self.get_rebalanced_weights(target_weights)
            # Execute trades
            if self._process_trades(trades, prices.loc[date], simulate=True):
                executed_info = self._process_trades(trades, prices.loc[date], simulate=False)

                for ticker, info in executed_info.items():
                    self._log_trade(
                        date=date,
                        ticker=ticker,
                        side="BUY" if trades[ticker] > 0 else "SELL",
                        quantity=info["qty"],
                        signal_price=prices.loc[date, ticker],
                        exec_price=info["price"],
                        strategy=self.strategy.capital_allocation  # pass in current strategy name
                    )
            else:
                self.execution_log.append({
                    "Date": date,
                    "Note": "Rebalance skipped — insufficient capital or holdings"
                })
            # Log account state
            self._log_account(date, prices.loc[date])
        print('Backtest completed.')
        # --- Extract equity curve and returns ---
        account_df = pd.DataFrame(self.account_history).set_index("Date").sort_index()
        equity_curve = account_df["Total Value"]
        returns = account_df["Total Value"].pct_change().dropna()

        return equity_curve, returns

    def _log_trade(self, date, ticker, side, quantity, signal_price, exec_price, strategy):
        self.trade_log.append({
            "Date": date,
            "Ticker": ticker,
            "Side": side,
            "Quantity": quantity,
            "Signal Price": signal_price,
            "Execution Price": exec_price,
            "Strategy": strategy
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



def main(tickers, strat, benchmark_ticker, benchmark_strat, start_date, end_date, slippage=0.001, commission=0.0005):
    # Run backtest
    cost_model = TransactionCostModel()
    strat_engine = BacktestEngine(tickers, strat, cost_model, start_date, end_date, slippage=slippage, commission=commission)
    strat_equity, strat_returns = strat_engine.run()

    # Benchmark = SPY
    bmk_engine = BacktestEngine([benchmark_ticker], benchmark_strat, cost_model, start_date, end_date, slippage=slippage, commission=commission)
    bmk_equity, bmk_returns = bmk_engine.run()

    strat_performance = PerformanceStats(strat_equity, bmk_returns, strat_returns, bmk_equity, strat_engine.trade_log, strat_engine.holdings)
    performance_stats = strat_performance._calculate_performance()
    alpha, beta = strat_performance._calc_alpha_beta(strat_returns, bmk_returns)
    rolling_stats = strat_performance._calculate_rolling_stats()
    exposure_stats = strat_performance._calculate_exposures()
    attribution_stats = strat_performance._calculate_attribution()
    summarised_trades = strat_performance._summarize_trades()
    return {
        "performance_stats": performance_stats,
        "alpha": alpha,
        "beta": beta,
        "rolling_stats": rolling_stats,
        "exposure_stats": exposure_stats,
        "attribution_stats": attribution_stats,
        "summarised_trades": summarised_trades
    }


if __name__ == '__main__':
    tickers = ["AAPL", "MSFT", "GOOG", "TSLA"]
    start = "2020-01-01"
    end = "2024-12-31"
    vol_data = GetSeries(ticker=tickers, start=start, end=end).fetch_volatility()   # Needed for volatility scaled allocator

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
    print('Ensemble Weights:', ensemble.aggregate_allocations())

    benchmark = InitialiseStrategy(
        strategy_cls=BuyAndHoldStrategy,
        allocator_cls=EqualWeightAllocator,
        tickers="SPY",
        start=start,
        end=end
    )
    main(
        tickers,
        ensemble,
        benchmark_ticker="SPY",
        benchmark_strat=benchmark,
        start_date=start,
        end_date=end,
        slippage=0.001,
        commission=0.0005
    )



