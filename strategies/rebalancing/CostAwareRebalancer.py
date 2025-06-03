import numpy as np
from strategies.rebalancing.base_rebalancer import BaseRebalancer

class CostAwareRebalancer:
    def __init__(self, trading_costs: dict, max_total_cost: float = None):
        """
        trading_costs: dict of {ticker: cost per unit weight traded}
        max_total_cost: optional cap on total transaction cost
        """
        self.trading_costs = trading_costs
        self.max_total_cost = max_total_cost

    def rebalance(self, current_weights: dict, target_weights: dict) -> tuple:
        """
        Minimizes trading cost to get close to target weights.
        Returns a tuple: (trades, new_weights)
        """
        all_tickers = set(current_weights.keys()).union(target_weights.keys())
        trades = {}
        total_cost = 0.0
        new_weights = current_weights.copy()

        # Greedy cost-minimizing trade execution (sorted by cost efficiency)
        deltas = {
            ticker: target_weights.get(ticker, 0.0) - current_weights.get(ticker, 0.0)
            for ticker in all_tickers
        }

        sorted_tickers = sorted(deltas.items(), key=lambda x: abs(x[1]) * self.trading_costs.get(x[0], 0))

        for ticker, delta in sorted_tickers:
            cost_per_unit = self.trading_costs.get(ticker, 0.0)
            trade_cost = abs(delta) * cost_per_unit

            if self.max_total_cost is not None and total_cost + trade_cost > self.max_total_cost:
                # Reduce trade size proportionally to stay under cost budget
                max_affordable_delta = (self.max_total_cost - total_cost) / cost_per_unit
                direction = np.sign(delta)
                trades[ticker] = direction * max_affordable_delta
                new_weights[ticker] = new_weights.get(ticker, 0.0) + trades[ticker]
                total_cost += abs(trades[ticker]) * cost_per_unit
                break
            else:
                trades[ticker] = delta
                new_weights[ticker] = target_weights.get(ticker, 0.0)
                total_cost += trade_cost

        return trades, new_weights


if __name__ == "__main__":
    # Example usage
    current_weights = {'AAPL': 0.2, 'GOOGL': 0.3, 'MSFT': 0.5}
    target_weights = {'AAPL': 0.4, 'GOOGL': 0.2, 'MSFT': 0.4}

    rebalancer = CostAwareRebalancer()
    trades, rebalanced_weights = rebalancer.rebalance(current_weights, target_weights)
    print(trades)  # Output: {'AAPL': 0.2, 'GOOGL': -0.1, 'MSFT': -0.1}