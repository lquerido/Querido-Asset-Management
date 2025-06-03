from strategies.allocations.BaseAllocator import BaseAllocator

class EqualWeightAllocator(BaseAllocator):
    def allocate(self, signals: dict) -> dict:
        active = {k: v for k, v in signals.items() if v != 0}
        n = len(active)
        weights = {k: 1/n if k in active else 0 for k in signals} if n > 0 else {k: 0 for k in signals}
        return self._add_cash_allocation(weights)

