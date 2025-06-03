class BaseAllocator:
    def allocate(self, signals: dict) -> dict:
        raise NotImplementedError
