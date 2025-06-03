from strategies.signal_generation.BaseStrategy import BaseStrategy
from strategies.allocations.EqualWeightAllocator import EqualWeightAllocator
from datasets.GetPriceSeries import GetPriceSeries

class MeanReversionStrategy(BaseStrategy):
    """
    Gets the position (buy, sell or hold) for each ticker based on mean reversion strategy.
    The mean reversion strategy estimates the z-score of the last price against a rolling mean and standard deviation over a specified lookback period.
    """
    def __init__(self, data: dict, lookback: int = 20, bound: float = 0.5):
        super().__init__(data)
        self.lookback = lookback
        self.bound = bound

    def generate_positions(self) -> dict:
        positions = {}
        for ticker, series in self.data.items():
            if len(series) < self.lookback:
                continue
            zscore = (series.iloc[-1] - series[-self.lookback:].mean()) / series[-self.lookback:].std()
            if zscore < -self.bound:
                positions[ticker] = 1.0
            elif zscore > self.bound:
                positions[ticker] = -1.0
            else:
                positions[ticker] = 0.0
        return positions


if __name__ == '__main__':
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    prices = GetPriceSeries(ticker=tickers, start="2020-01-01", end="2024-12-31").fetch()
    strategy = MeanReversionStrategy(prices, lookback=20, bound=0.5)
    signals = strategy.generate_positions()
    weights = EqualWeightAllocator().allocate(signals)
    print("Current Signal:", signals)

