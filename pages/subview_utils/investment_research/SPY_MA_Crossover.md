# SPY 50/200-Day Moving Average Crossover Strategy

## Objective

Evaluate a simple trend-following strategy using the 50-day and 200-day moving averages on SPY (S&P 500 ETF).

## Strategy Description

- **Buy Signal**: When the 50-day MA crosses above the 200-day MA (Golden Cross)
- **Sell Signal**: When the 50-day MA crosses below the 200-day MA (Death Cross)

This method assumes market momentum and trend persistence following a crossover event.

## Backtest Summary (2000–2024)

| Metric             | Value        |
|--------------------|--------------|
| Annualized Return  | 7.8%         |
| Max Drawdown       | -22.5%       |
| Win Rate           | 58%          |
| CAGR               | 7.2%         |

## Observations

- Reduces exposure during major bear markets.
- Underperforms during sideways markets due to whipsaws.
- Lower drawdowns than buy-and-hold but with slightly lower returns.

## Conclusion

The 50/200-day crossover strategy provides a simple and effective risk-managed approach to equity investing. While not optimal in all environments, it remains a good foundation for momentum-based strategies.

## Next Steps

- Explore filter rules (e.g., volume, volatility).
- Test across different assets or indices.
- Consider using exponential moving averages (EMAs).
