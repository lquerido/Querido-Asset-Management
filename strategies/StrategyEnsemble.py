from strategies.signal_generation.MeanReversionStrategy import MeanReversionStrategy
from strategies.signal_generation.MomentumStrategy import MomentumStrategy
from strategies.allocations.VolatilityScaledAllocator import VolatilityScaledAllocator
from strategies.InitialiseStrategy import InitialiseStrategy
from datasets.GetSeries import GetSeries

class StrategyEnsemble:
    def __init__(self, capital_allocation: dict):
        """
        capital_allocation: {strategy_name: (initialised_strategy_instance, capital_fraction)}
        """
        self.capital_allocation = capital_allocation

    def aggregate_allocations(self) -> dict:
        combined = {}
        for name, (strategy_runner, capital_fraction) in self.capital_allocation.items():
            _, strat_weights = strategy_runner.run()  # signals, weights

            for ticker, weight in strat_weights.items():
                scaled_weight = weight * capital_fraction
                combined[ticker] = combined.get(ticker, 0) + scaled_weight

        return combined


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
    weights = ensemble.aggregate_allocations()
    print("Ensemble Weights:", weights)
