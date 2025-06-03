from strategies.signal_generation.BaseStrategy import BaseStrategy
from strategies.allocations.VolatilityScaledAllocator import VolatilityScaledAllocator
from datasets.GetPriceSeries import GetSeries

class MomentumStrategy(BaseStrategy):
    def __init__(self, data: dict, lookback: int = 20, threshold: float = 0.02):
        super().__init__(data)
        self.lookback = lookback
        self.threshold = threshold

    def generate_positions(self) -> dict:
        positions = {}
        for ticker, series in self.data.items():
            if len(series) < self.lookback + 1:
                continue

            past_price = series.iloc[-self.lookback - 1]
            current_price = series.iloc[-1]
            momentum = (current_price - past_price) / past_price

            if momentum > self.threshold:
                positions[ticker] = 1.0  # Long
            elif momentum < -self.threshold:
                positions[ticker] = -1.0  # Short
            else:
                positions[ticker] = 0.0  # Neutral

        return positions


if __name__ == '__main__':
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    prices = GetSeries(ticker=tickers, start="2020-01-01", end="2024-12-31").fetch_prices()
    vols = GetSeries(ticker=tickers, start="2020-01-01", end="2024-12-31").fetch_volatility()
    strategy = MomentumStrategy(prices, lookback=20, threshold=0.02)
    signals = strategy.generate_positions()
    weights = VolatilityScaledAllocator(vol_data=vols).allocate(signals)
    print("Current Signal:", signals)