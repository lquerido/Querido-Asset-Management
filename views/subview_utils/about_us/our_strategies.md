# Our Strategies

Our portfolio combines distinct alpha-generating models, each trading its own universe and logic. Capital is allocated dynamically based on performance and orthogonality.

---

## Current Strategies

### 1. Z-Score Mean Reversion
- **Objective:** Buy when prices are statistically cheap, sell when expensive
- **Universe:** Large-cap US equities
- **Signal:** ±2 std dev from 20-day mean

### 2. Momentum Overlay
- **Objective:** Capture trend continuation in high-momentum names
- **Lookback:** 20 days
- **Trigger:** Momentum > 2% or < -2%

### 3. Macro Filter
- **Objective:** Enhance signal quality with macro filters like PMI, rates, and inflation
- **Source:** FRED

---

## Risk Management

- Position sizing based on volatility
- Maximum exposure caps
- Strategy diversification

---

## Capital Allocation

We use an ensemble weighting method, updated quarterly, to allocate capital across strategies.
