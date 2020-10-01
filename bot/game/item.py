from bot.database.models import Item as ItemModel
from dataclasses import dataclass

from bot.utils.errors import ItemNotFoundError


@dataclass
class Item:
    id: int
    name: str
    description: str
    cost: int
    creation_id: int

    @classmethod
    async def load(cls, id: int = None, name: str = None, description: str = None, cost: int = None, creation_id: int = None):
        item_obj = (
            await ItemModel.query.where(ItemModel.name == name)
            .gino.first()
        )

        if item_obj is None:
            raise ItemNotFoundError(name)

        return item_obj


