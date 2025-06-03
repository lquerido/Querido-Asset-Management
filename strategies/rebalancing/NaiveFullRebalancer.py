import numpy as np
from strategies.rebalancing.BaseRebalancer import BaseRebalancer

class NaiveFullRebalancer:
    def __init__(self):
        pass

    def rebalance(self, current_weights: dict, target_weights: dict) -> tuple:
        """
        Always rebalance fully to target weights.
        Returns a tuple: (trades, new_weights)
        """
        all_tickers = set(current_weights.keys()).union(target_weights.keys())
        trades = {}
        new_weights = {}
        for ticker in all_tickers:
            current = current_weights.get(ticker, 0.0)
            target = target_weights.get(ticker, 0.0)
            trades[ticker] = target - current
            new_weights[ticker] = target
        return trades, new_weights


if __name__ == "__main__":
    # Example usage
    current_weights = {'AAPL': 0.2, 'GOOGL': 0.3, 'MSFT': 0.5}
    target_weights = {'AAPL': 0.4, 'GOOGL': 0.2, 'MSFT': 0.4}

    rebalancer = NaiveFullRebalancer()
    trades, rebalanced_weights = rebalancer.rebalance(current_weights, target_weights)
    print(trades)  # Output: {'AAPL': 0.2, 'GOOGL': -0.1, 'MSFT': -0.1}