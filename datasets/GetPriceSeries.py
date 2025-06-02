import yfinance as yf
import pandas as pd

class GetPriceSeries:
    def __init__(self, ticker="SPY", start="2018-01-01", end="2024-12-31"):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.data = self.fetch()

    def fetch(self):
        df = yf.download(self.ticker, start=self.start, end=self.end)
        df = df[["Close"]].rename(columns={"Close": "Price"})
        df.index.name = "Date"
        return df

if __name__ == "__main__":
    ticker = yf.Ticker("AAPL")
    sector = ticker.info.get("sector", "Unknown")
    [print(f"{k}: {v}") for k, v in ticker.info.items()]
    print(f"AAPL Sector: {sector}")