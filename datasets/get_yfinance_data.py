import yfinance as yf
import pandas as pd

def get_price_data(ticker="SPY", start="2018-01-01", end="2024-12-31"):
    df = yf.download(ticker, start=start, end=end)
    df = df[["Adj Close"]].rename(columns={"Adj Close": "Price"})
    df["Returns"] = df["Price"].pct_change().fillna(0)
    return df

if __name__ == "__main__":
    price_data = get_price_data()
    print('Done')