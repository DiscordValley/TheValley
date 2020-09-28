from dataclasses import dataclass


@dataclass
class InventoryItem:
    inventory_id: int
    item_id: int
    quantity: int
    name: str
    description: str
    cost: int
    creation_id: int

    @classmethod
    async def load(
        cls, inventory_id: int, item_id: int, quantity: int
    ) -> "InventoryItem":
        """Fully load a Inventory item with information from items table"""
        pass

    async def fetch(self):
        """Fetch information from items table if not previously loaded"""
        pass
