from strategies.signal_generation.BaseStrategy import BaseStrategy
from strategies.allocations.EqualWeightAllocator import EqualWeightAllocator
from datasets.GetSeries import GetSeries

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
                positions[ticker] = -1.0        # Todo: What do we did with sell positions? Do we close out any open positions? Do we short (perhaps need an input for say 130/30) - in which case do we need to model leverage?
            else:
                positions[ticker] = 0.0
        return positions


if __name__ == '__main__':
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    prices = GetSeries(ticker=tickers, start="2020-01-01", end="2024-12-31").fetch_prices()
    strategy = MeanReversionStrategy(prices, lookback=20, bound=0.5)
    signals = strategy.generate_positions()
    weights = EqualWeightAllocator().allocate(signals)
    print("Current Signal:", signals)

