class BaseAllocator:
    def allocate(self, signals: dict) -> dict:
        raise NotImplementedError

    def _normalize_weights(self, weights: dict) -> dict:         # Todo: Consider how we handle no signal
        total_weight = sum(weights.values())
        if total_weight == 0:
            # return {"CASH": 1.0}
            return {"AAPL": 1.0}  # Default to a single asset with full weight if no signals are present        # Todo: Allocate to the index?
        weights = {k: w / total_weight for k, w in weights.items()}
        return weights