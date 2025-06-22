# Comparing Volatility Estimation Methods

## Objective

Explore different methods of estimating volatility and examine how their assumptions and outputs differ in practical use.

## Methods Compared

### 1. **Historical Volatility**
- **Definition**: Standard deviation of past returns over a fixed window.
- **Pros**: Simple, fast.
- **Cons**: Lags during regime shifts.

### 2. **Exponentially Weighted Moving Average (EWMA)**
- **Definition**: Weights recent returns more heavily; reacts faster to new information.
- **Pros**: Captures changing volatility better.
- **Cons**: Sensitive to the choice of lambda (smoothing parameter).

### 3. **GARCH(1,1)**
- **Definition**: Models volatility as a function of past variances and returns.
- **Pros**: Captures volatility clustering and persistence.
- **Cons**: More complex and computationally intensive.

### 4. **Implied Volatility**
- **Definition**: Derived from option prices (e.g., VIX for SPY).
- **Pros**: Forward-looking.
- **Cons**: Reflects market sentiment and supply/demand distortions.

## Example (SPY, Jan 2020–Jan 2024)

| Method       | Avg. Vol (%) | Reactivity | Lag Risk | Interpretability |
|--------------|--------------|------------|----------|------------------|
| Historical   | 18.2         | Low        | High     | High             |
| EWMA         | 19.6         | Medium     | Medium   | Medium           |
| GARCH(1,1)   | 20.4         | High       | Low      | Low              |
| Implied (VIX)| 22.1         | Very High  | None     | Medium           |

## Conclusion

Different volatility models suit different needs:
- **Historical** for simplicity.
- **EWMA** and **GARCH** for dynamic strategies.
- **Implied** for market-driven forecasting.

## Next Steps

- Integrate volatility models into risk-adjusted return metrics.
- Explore model combinations or regime-switching approaches.
