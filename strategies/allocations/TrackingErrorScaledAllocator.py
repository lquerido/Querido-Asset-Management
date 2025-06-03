import numpy as np
import pandas as pd
from allocators.base_allocator import BaseAllocator

class TrackingErrorAllocator(BaseAllocator):
    def __init__(self, benchmark_weights: dict, risk_budget: float = 0.05):
        self.benchmark_weights = benchmark_weights
        self.risk_budget = risk_budget

    def allocate(self, signals: dict, covariance: pd.DataFrame) -> dict:
        """
        signals: {ticker: signal strength (can be -1, 0, 1 or continuous)}
        covariance: asset return covariance matrix (daily)
        """
        tickers = list(signals.keys())
        signal_vec = np.array([signals[t] for t in tickers])
        bm_vec = np.array([self.benchmark_weights.get(t, 0) for t in tickers])

        # Normalize signals to be a delta over benchmark
        signal_delta = signal_vec - bm_vec

        if np.all(signal_delta == 0):
            return dict(zip(tickers, bm_vec))  # no signal = hold benchmark

        # Scale delta to respect tracking error constraint
        delta_var = signal_delta @ covariance.loc[tickers, tickers].values @ signal_delta.T
        scale = self.risk_budget / np.sqrt(252 * delta_var) if delta_var > 0 else 0

        final_weights = bm_vec + scale * signal_delta
        return dict(zip(tickers, final_weights))
