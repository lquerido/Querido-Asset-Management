class BaseStrategy:
    def __init__(self, data: dict):
        self.data = data  # dict of {ticker: pd.Series}

    def generate_positions(self) -> dict:
        raise NotImplementedError("Implement in subclass")
