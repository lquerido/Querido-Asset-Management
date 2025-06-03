class BaseAllocator:
    def allocate(self, signals: dict) -> dict:
        raise NotImplementedError

    def _add_cash_allocation(self, weights: dict) -> dict:      # Todo: Can this be merged into the allocate method? Otherwise we have to call it with every allocator
        total_weight = sum(weights.values())
        if total_weight < 1.0:
            weights["CASH"] = 1.0 - total_weight
        return weights