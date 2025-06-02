from strategies.BuyLowSellHigh import MeanReversionStrategy
from strategies.MomentumStrategy import MomentumStrategy
from datasets.GetPriceSeries import GetPriceSeries

class StrategyEnsemble:
    def __init__(self, strategies: dict, allocations: dict):
        self.strategies = strategies  # {name: strategy_instance}
        self.allocations = allocations  # {name: capital_fraction}

    def aggregate_positions(self) -> dict:
        combined = {}

        for name, strategy in self.strategies.items():
            alloc = self.allocations.get(name, 0)
            strat_positions = strategy.generate_positions()

            for ticker, pos in strat_positions.items():
                scaled_pos = pos * alloc
                combined[ticker] = combined.get(ticker, 0) + scaled_pos

        return combined  # Final portfolio {ticker: weight}


if __name__ == '__main__':
    # Get Price Series for selected tickers
    series_aapl = GetPriceSeries(ticker="AAPL", start="2018-01-01", end="2024-12-31")
    series_msft = GetPriceSeries(ticker="MSFT", start="2018-01-01", end="2024-12-31")
    series_goog = GetPriceSeries(ticker="GOOG", start="2018-01-01", end="2024-12-31")
    series_tsla = GetPriceSeries(ticker="TSLA", start="2018-01-01", end="2024-12-31")

    mean_rev_data = {"AAPL": series_aapl, "MSFT": series_msft}
    momentum_data = {"GOOG": series_goog, "TSLA": series_tsla}

    mean_rev = MeanReversionStrategy(mean_rev_data)
    momentum = MomentumStrategy(momentum_data)

    strategies = {
        "mean_reversion": mean_rev,
        "momentum": momentum
    }
    allocations = {
        "mean_reversion": 0.6,
        "momentum": 0.4
    }

    ensemble = StrategyEnsemble(strategies, allocations)
    portfolio = ensemble.aggregate_positions()
