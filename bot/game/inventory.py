from dataclasses import dataclass
from bot.database.models import Inventory as InventoryModel
from bot.game.item import InventoryItem
from typing import Dict


@dataclass
class Inventory:
    player_id: int
    items: Dict[int, InventoryItem]

    @classmethod
    async def load(cls, player_id: int, full: bool = True):
        """Load a players Inventory
        optional param: full - also load information for all items"""
        items = await InventoryModel.query.where(
            InventoryModel.player_id == player_id
        ).gino.all()
        inventory_items = dict()
        for item in items:
            item_data = await InventoryItem.load(
                inventory_id=item.id,
                item_id=item.item_id,
                quantity=item.quantity,
                full=full,
            )
            inventory_items[item_data.item_id] = item_data

        return Inventory(player_id=player_id, items=inventory_items)

    async def fetch(self):
        """Fetch information about inventory items if not previously loaded"""
        for item in self.items.values():
            await item.fetch()
