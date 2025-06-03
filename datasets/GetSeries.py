import yfinance as yf
import pandas as pd
import numpy as np

class GetSeries:
    def __init__(self, ticker="SPY", start="2018-01-01", end="2024-12-31", freq="D", window=None, annualise_vol=True):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.freq = freq.upper()
        self.window = window  # None means use all data
        self.annualise_vol = annualise_vol

    def fetch_prices(self):
        df = yf.download(self.ticker, start=self.start, end=self.end)
        df = df[["Close"]].rename(columns={"Close": "Price"})
        df.columns = df.columns.get_level_values(1)
        df.index = pd.to_datetime(df.index)
        df = df.resample(self.freq).last().dropna()  # use last closing price in each period
        df.index.name = "Date"
        return df

    def fetch_returns(self):
        df_prices = self.fetch_prices()
        df_returns = df_prices.pct_change().dropna()
        return df_returns

    def fetch_volatility(self):
        returns = self.fetch_returns()
        # Determine periods per year based on frequency
        freq_map = {
            "D": 252,
            "W": 52,
            "M": 12,
            "Q": 4,
            "Y": 1
        }
        periods_per_year = freq_map.get(self.freq, 252) if self.annualise_vol else 1
        # Use rolling or full-period std depending on self.window
        if not self.window:
            self.window = len(returns)
        clipped_returns = returns.iloc[-self.window:,]
        vols = clipped_returns.std() * np.sqrt(periods_per_year)
        return vols.to_dict()


if __name__ == "__main__":
    # Get prices
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    price = GetSeries(tickers, start="2020-01-01", end="2024-12-31").fetch_prices()
    # Get security vols
    vol = GetSeries(tickers, start="2020-01-01", end="2024-12-31").fetch_volatility()
    # Get security metadata
    ticker = yf.Ticker("AAPL")
    sector = ticker.info.get("sector", "Unknown")
    [print(f"{k}: {v}") for k, v in ticker.info.items()]
    print(f"AAPL Sector: {sector}")