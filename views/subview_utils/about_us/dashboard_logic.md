# Dashboard Logic

This dashboard provides a modular, transparent view into the architecture and performance of our quantitative investment strategies.

---

## Backtesting Framework

All strategies are evaluated using a robust backtesting engine that supports:

- **Out-of-sample validation**: All results shown are strictly based on unseen data.
- **Trading frictions**: Simulations include realistic assumptions for slippage, trading costs, and bid-ask spreads.
- **Leverage**: Strategies may apply leverage, bounded by portfolio-level risk controls.
- **Execution logic**: Buy/sell signals are translated into positions at the next available price, not hindsight-optimized fills.

---

## Strategy Layer

Each strategy operates independently:
- It receives its own data (macro, price, etc.)
- Generates signals and allocates across its defined universe
- Outputs position weights or trades
- Can be used standalone or as part of the composite portfolio

---

## Composite Portfolio Logic

We allocate capital across strategies using an ensemble model that:
- Assigns weights to each strategy
- Normalizes overlapping positions
- Aggregates signals across different universes
- Manages portfolio risk and exposure holistically

---

## Performance Metrics

We show both simple and advanced metrics:
- **Simple**: Cumulative returns, drawdowns, top/bottom trades
- **Advanced**: Attribution, turnover, holding period, Sharpe, Sortino, etc.
- **Risk**: VaR, correlation heatmaps, exposure breakdowns

---

## Update Cycle

- Strategy parameters are trained only on in-sample data
- Dashboards and reports are updated **quarterly**
- New research papers and strategies are published as they are finalized

---

For more detail, check out our [GitHub repository](https://github.com) or contact us directly.
