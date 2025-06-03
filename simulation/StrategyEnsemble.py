from strategies.signal_generation.MeanReversionStrategy import MeanReversionStrategy
from strategies.signal_generation.MomentumStrategy import MomentumStrategy
from datasets.GetSeries import GetSeries

class StrategyEnsemble:
    def __init__(self, capital_allocation: dict):
        self.capital_allocation = capital_allocation  # {strategy_instance: capital_fraction}

    def aggregate_allocations(self) -> dict:
        combined = {}
        for strategy, capital_fraction in self.capital_allocation.items():
            alloc = self.capital_allocation.get(strategy, 0)
            strat_positions = strategy.generate_positions()

            for ticker, pos in strat_positions.items():
                scaled_pos = pos * alloc
                combined[ticker] = combined.get(ticker, 0) + scaled_pos

        return combined  # Final portfolio {ticker: weight}


if __name__ == '__main__':
    # Get Price Series for selected tickers
    tickers = ["AAPL", "MSFT", "GOOG", "TSLA"]
    prices = GetSeries(ticker=tickers, start="2020-01-01", end="2024-12-31").fetch_prices()
    capital_allocation = {"mean_reversion": 0.5, "momentum": 0.3, "macro_filter": 0.2}
    ensemble_weights = StrategyEnsemble(capital_allocation).aggregate_allocations()
    print("Aggregated Allocations:", ensemble_weights)
