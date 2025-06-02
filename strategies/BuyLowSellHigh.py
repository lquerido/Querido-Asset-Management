from strategies import BaseStrategy

class MeanReversionStrategy(BaseStrategy):
    def generate_positions(self) -> dict:
        positions = {}
        for ticker, series in self.data.items():
            if len(series) < 20:
                continue
            zscore = (series.iloc[-1] - series[-20:].mean()) / series[-20:].std()
            if zscore < -2:
                positions[ticker] = 1.0
            elif zscore > 2:
                positions[ticker] = -1.0
            else:
                positions[ticker] = 0.0
        return positions


# if __name__ == '__main__':
#     prices = pd.Series(np.random.randn(100).cumsum() + 100)
#     strategy = MeanRevertingProcess(prices)
#     current_signal = strategy.generate_signal()
#     print("Current Signal:", current_signal)

