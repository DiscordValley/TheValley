import random
from dataclasses import dataclass
from typing import Tuple, Union, List, Optional

import ujson

# from bot.database.models import Inventory as InventoryModel
# from bot.database.models import Item as ItemModel
from bot.database.models import Player as PlayerModel
from bot.game.inventory import Inventory
from bot.game.item import InventoryItem
from bot.utils.errors import InvalidQuantityError, InsufficientFundsError

with open("levels.json", "r") as f:
    LEVELS = ujson.load(f)


def xp_formula(player_db: PlayerModel, modifier: float):
    if player_db.level > 4:
        xp = player_db.xp + abs(
            int(
                (
                    (
                        (
                            1
                            * random.randint(1, 10)
                            * abs(player_db.level - (player_db.level * 0.4))
                        )
                        / (5 * 1)
                    )
                    * (
                        (
                            pow(
                                (
                                    (2 * abs(player_db.level - (player_db.level * 0.4)))
                                    + 10
                                ),
                                2.5,
                            )
                            / pow(
                                (
                                    abs(player_db.level - (player_db.level * 0.4))
                                    + player_db.level
                                    + 10
                                ),
                                2.5,
                            )
                        )
                        + 1
                    )
                    * modifier
                )
            )
        )
    else:
        xp = player_db.xp + abs(random.randint(1, 5))
    return xp


@dataclass
class Player:
    id: int
    user_id: int
    balance: int
    xp: int
    level: int
    energy: int
    db_object: PlayerModel
    inventory: Optional[Inventory] = None

    @classmethod
    async def load(
        cls,
        user_id: int = None,
        guild_id: int = None,
        player_obj: PlayerModel = None,
        db_object: bool = False,
        load_inventory: bool = False,
        load_inventory_fully: bool = True,
    ) -> Union["Player", Tuple["Player", PlayerModel]]:
        """Load a player
        - either through user-id + guild-id or by already providing a player_obj database object
        - optional flags:
            - db_object: return raw database object as well Tuple[Player, PlayerModel]
                default: false
            - load_inventory: automatically load inventory
                default: false
            - load_inventory_fully: if loading the inventory, also fetch all item information (name, description etc.)
                default: true

        """
        if player_obj:
            player_db = player_obj
        else:
            player_db = (
                await PlayerModel.query.where(PlayerModel.user_id == user_id)
                .where(PlayerModel.guild_id == guild_id)
                .gino.first()
            )
            if player_db is None:
                player_db = await PlayerModel.create(user_id=user_id, guild_id=guild_id)
        player = Player(
            id=player_db.id,
            user_id=player_db.user_id,
            balance=player_db.balance,
            xp=player_db.xp,
            level=player_db.level,
            energy=player_db.energy,
            db_object=player_db,
        )
        if load_inventory:
            await player.load_inventory(full=load_inventory_fully)
        if db_object:
            return player, player_db
        else:
            return player

    async def load_inventory(self, full: True):
        """full: whether or not to load the full item information (name, description etc.)"""
        self.inventory = await Inventory.load(player_id=self.id, full=full)

    @classmethod
    async def top(cls, guild_id: int) -> List["Player"]:
        leaders = (
            await PlayerModel.query.where(PlayerModel.guild_id == guild_id)
            .order_by(PlayerModel.xp.desc())
            .limit(5)
            .gino.all()
        )
        players = list()
        for leader in leaders:
            players.append(await Player.load(player_obj=leader))
        return players

    async def validate_sell(self, item_id: int, quantity: Union[int, str]) -> int:
        if not self.inventory:
            await self.load_inventory(full=True)
        item = self.inventory.get_item(item_id)
        if isinstance(quantity, str):
            if quantity.lower() == "all":
                quantity = item.quantity
            else:
                raise InvalidQuantityError(quantity)
        if isinstance(quantity, int) and item.quantity < quantity:
            quantity = item.quantity

        return quantity

    async def sell(
        self,
        item: InventoryItem,
        quantity: int,
    ) -> Tuple[int, int]:

        sold_price = item.cost * quantity
        await self.inventory.remove_item(item.item_id, quantity)
        await self.add_balance(sold_price)
        return sold_price, self.balance

    async def add_balance(self, amount: int):
        new_balance = self.balance + amount
        await self.db_object.update(balance=new_balance).apply()
        self.balance = new_balance

    async def remove_balance(self, amount: int):
        if self.balance < amount:
            raise InsufficientFundsError(balance=self.balance, amount=amount)
        new_balance = self.balance - amount
        await self.db_object.update(balance=new_balance).apply()
        self.balance = new_balance

    @classmethod
    async def update_xp(cls, user_id, guild_id, modifier) -> Tuple["Player", bool]:
        """**Use to give XP after a successful command.**

        USAGE:
        player, leveled_up = await Player.update_xp(
            user_id=message.author.id, guild_id=message.guild.id, modifier=0
        )

        """
        player, player_db = await Player.load(
            user_id=user_id, guild_id=guild_id, db_object=True
        )

        modifier += 0.1

        xp = xp_formula(player_db, modifier)

        await player_db.update(xp=xp).apply()

        og_level = player_db.level

        player_level = 1
        for level, xp in LEVELS.items():
            if player_db.xp >= xp:
                player_level = level
            else:
                break

        await player_db.update(level=int(player_level)).apply()

        return (
            player,
            player_level != og_level,
        )
