import datetime
import yfinance as yf
from datasets.GetSeries import GetSeries
from strategies.signal_generation.MomentumStrategy import MomentumStrategy
from strategies.signal_generation.MeanReversionStrategy import MeanReversionStrategy
from strategies.allocations.VolatilityScaledAllocator import VolatilityScaledAllocator


class InitialiseStrategy:
    def __init__(self, strategy_cls, allocator_cls, tickers, start, end, strategy_kwargs=None, allocator_kwargs=None):
        self.tickers = tickers
        self.start = start
        self.end = end
        self.strategy_cls = strategy_cls
        self.allocator_cls = allocator_cls
        self.strategy_kwargs = strategy_kwargs or {}
        self.allocator_kwargs = allocator_kwargs or {}

        self.data = GetSeries(ticker=tickers, start=start, end=end).fetch_prices()
        self.vol = GetSeries(ticker=tickers, start=start, end=end).fetch_volatility()

    def run(self):
        strategy = self.strategy_cls(data=self.data, **self.strategy_kwargs)
        signals = strategy.generate_positions()
        allocator = self.allocator_cls(**self.allocator_kwargs)
        weights = allocator.allocate(signals)
        return signals, weights


if __name__ == '__main__':
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

    strategy1 = InitialiseStrategy(
        strategy_cls=MomentumStrategy,
        allocator_cls=VolatilityScaledAllocator,
        tickers=tickers,
        start="2020-01-01",
        end="2024-12-31",
        strategy_kwargs={"lookback": 20, "threshold": 0.02}
    )

    signals, weights = strategy1.run()
    print("Signals:", signals)
    print("Weights:", weights)
    print('Done')
