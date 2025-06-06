from strategies.allocations.BaseAllocator import BaseAllocator

class VolatilityScaledAllocator(BaseAllocator):
    def __init__(self, vol_data: dict):  # {ticker: volatility}
        self.vol_data = vol_data

    def allocate(self, signals: dict) -> dict:
        active = {k: v for k, v in signals.items() if v != 0}
        inv_vol = {k: 1 / self.vol_data[k] for k in active}
        total = sum(inv_vol.values())
        weights = {k: inv_vol[k] / total if k in active else 0 for k in signals}
        return self._normalize_weights(weights)
