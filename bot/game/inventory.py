from dataclasses import dataclass
from bot.database.models import Inventory as InventoryModel
from bot.game.item import InventoryItem
from typing import Dict, Optional
from bot.utils.errors import InsufficientQuantityError


@dataclass
class Inventory:
    player_id: int
    items: Dict[int, InventoryItem]
    full: bool

    @classmethod
    async def load(cls, player_id: int, full: bool = True):
        """Load a players Inventory
        optional param: full - also load information for all items"""
        inventory = Inventory(player_id=player_id, items=dict(), full=full)
        await inventory.reload_items()
        return inventory

    async def reload_items(self):
        items = await InventoryModel.query.where(
            InventoryModel.player_id == self.player_id
        ).gino.all()
        inventory_items = dict()
        for item in items:
            item_data = await InventoryItem.load(
                inventory_id=item.id,
                item_id=item.item_id,
                quantity=item.quantity,
                full=self.full,
            )
            inventory_items[item_data.item_id] = item_data
        self.items = inventory_items

    def get_item(self, item_id: int) -> Optional[InventoryItem]:
        return self.items.get(item_id)

    def find_item(self, item_name: str) -> Optional[InventoryItem]:
        for item in self.items.values():
            if item.name == item_name:
                return item
        return None

    @staticmethod
    async def get_inventory_object(inventory_id: int):
        return await InventoryModel.get(inventory_id)

    async def remove_item(self, item_id: int, quantity: int = 1):
        item = self.get_item(item_id)

        if not item or item.quantity < quantity:
            raise InsufficientQuantityError(
                item.name, current_quantity=item.quantity, remove_quantity=quantity
            )
        else:
            inv_obj = await self.get_inventory_object(item.inventory_id)
            if inv_obj.quantity == quantity:
                await inv_obj.delete()
            else:
                await inv_obj.update(quantity=(inv_obj.quantity - quantity)).apply()
        await self.reload_items()

    async def add_item(self, item_id: int, quantity: int = 1):
        item = self.get_item(item_id)
        if not item:
            _ = await InventoryModel.create(
                player_id=self.player_id, item_id=item_id, quantity=quantity
            )
        else:
            inv_obj = await self.get_inventory_object(item.inventory_id)
            await inv_obj.update(quantity=inv_obj.quantity + quantity).apply()
        await self.reload_items()

    async def fetch(self):
        """Fetch information about inventory items if not previously loaded"""
        for item in self.items.values():
            await item.fetch()
        self.full = True
