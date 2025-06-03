class BaseRebalancer:
    def rebalance(self, current_weights: dict, target_weights: dict) -> dict:
        raise NotImplementedError