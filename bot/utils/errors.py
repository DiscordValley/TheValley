class ItemNotFoundError(Exception):
    def __init__(self, item: str):
        self.item = item


class InvalidQuantityError(Exception):
    def __init__(self, name: str):
        self.name = name
