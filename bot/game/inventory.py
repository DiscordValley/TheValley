from dataclasses import dataclass
from bot.database.models import Inventory as InventoryModel
from bot.game.item import InventoryItem
from typing import List


@dataclass
class Inventory:
    player_id: int
    items: List[InventoryItem]

    @classmethod
    async def load(cls, player_id: int, full: True):
        """Load a players Inventory
        optional param: full - also load information for all items"""
        pass
