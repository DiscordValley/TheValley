class ItemNotFoundError(Exception):
    def __init__(self, item: str):
        self.item = item


class InvalidQuantityError(Exception):
    def __init__(self, name: str):
        self.name = name


class InsufficientQuantityError(Exception):
    def __init__(self, name: str, current_quantity: int, remove_quantity: int):
        self.name = name
        self.current_quantity = current_quantity
        self.remove_quantity = remove_quantity
