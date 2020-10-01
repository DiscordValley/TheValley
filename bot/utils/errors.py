class ItemNotFoundError(Exception):
    def __init__(self, item: str):
        self.item = item


class NotAllString(Exception):
    def __init__(self, name: str):
        self.name = name
