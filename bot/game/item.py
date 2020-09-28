from dataclasses import dataclass
from typing import Optional

from bot.database.models.items import Item as ItemModel


@dataclass
class InventoryItem:
    inventory_id: int
    item_id: int
    quantity: int
    name: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[int] = None
    creation_id: Optional[int] = None

    @classmethod
    async def load(
        cls, inventory_id: int, item_id: int, quantity: int, full: bool = True
    ) -> "InventoryItem":
        """Fully load a Inventory item with information from items table"""
        item = InventoryItem(
            inventory_id=inventory_id, item_id=item_id, quantity=quantity
        )
        if full:
            await item.fetch()
        return item

    async def fetch(self):
        """Fetch information from items table if not previously loaded"""
        item = await ItemModel.get(self.item_id)
        if not item:
            raise ValueError(f"Item with id {self.item_id} not found in database.")
        self.name = item.name
        self.description = item.description
        self.cost = item.cost
        self.creation_id = item.creation_id
