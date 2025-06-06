from strategies.signal_generation.BaseStrategy import BaseStrategy
from strategies.allocations.EqualWeightAllocator import EqualWeightAllocator
from datasets.GetSeries import GetSeries

class BuyAndHoldStrategy(BaseStrategy):
    """
    Gets the position (buy, sell or hold) for each ticker based on mean reversion strategy.
    The mean reversion strategy estimates the z-score of the last price against a rolling mean and standard deviation over a specified lookback period.
    """
    def __init__(self, data: dict):
        super().__init__(data)

    def generate_positions(self) -> dict:
        positions = {}
        for ticker, series in self.data.items():
            positions[ticker] = 1
        return positions


if __name__ == '__main__':
    tickers = ['^SPX']
    prices = GetSeries(ticker=tickers, start="2020-01-01", end="2024-12-31").fetch_prices()
    strategy = BuyAndHoldStrategy(prices)
    signals = strategy.generate_positions()
    weights = EqualWeightAllocator().allocate(signals)
    print("Current Signal:", signals)

