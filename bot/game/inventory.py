from dataclasses import dataclass
from bot.database.models import Inventory as InventoryModel
from bot.game.item import InventoryItem
from typing import List


@dataclass
class Inventory:
    player_id: int
    items: List[InventoryItem]

    @classmethod
    async def load(cls, player_id: int, full: bool = True):
        """Load a players Inventory
        optional param: full - also load information for all items"""
        items = await InventoryModel.query.where(
            InventoryModel.player_id == player_id
        ).gino.all()
        inventory_items = list()
        for item in items:
            inventory_items.append(
                await InventoryItem.load(
                    inventory_id=item.id,
                    item_id=item.item_id,
                    quantity=item.quantity,
                    full=full,
                )
            )

        return Inventory(player_id=player_id, items=inventory_items)

    async def fetch(self):
        """Fetch information about inventory items if not previously loaded"""
        for item in self.items:
            await item.fetch()
