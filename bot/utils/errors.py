class ItemNotFoundError(Exception):
    def __init__(self, item: str):
        self.item = item
