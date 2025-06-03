class BaseAllocator:
    def allocate(self, signals: dict) -> dict:
        raise NotImplementedError

    def _add_cash_allocation(self, weights: dict) -> dict:
        total_weight = sum(weights.values())
        if total_weight < 1.0:
            weights["CASH"] = 1.0 - total_weight
        return weights