import random
from typing import Tuple, Union, List

import ujson

from bot.database.models import Player as PlayerModel
from bot.database.models import Item as ItemModel
from bot.database.models import Inventory as InventoryModel
from dataclasses import dataclass

from bot.utils.errors import ItemNotFoundError, NotAllString

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

    @classmethod
    async def load(
        cls,
        user_id: int = None,
        guild_id: int = None,
        player_obj: PlayerModel = None,
        db_object: bool = False,
    ) -> Union["Player", Tuple["Player", PlayerModel]]:
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
        )
        if db_object:
            return player, player_db
        else:
            return player

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

    @classmethod
    async def validate_sell(
        cls, player_id: int, item_id: int, quantity: Union[int, str]
    ) -> Tuple[InventoryModel, int]:
        inv_obj = (
            await InventoryModel.query.where(InventoryModel.player_id == player_id)
            .where(InventoryModel.item_id == item_id)
            .gino.first()
        )
        if isinstance(quantity, str):
            if quantity.lower() == "all":
                quantity = inv_obj.quantity
            else:
                raise NotAllString(quantity)
        if isinstance(quantity, int) and inv_obj.quantity < quantity:
            quantity = inv_obj.quantity

        return inv_obj, quantity

    @classmethod
    async def sell(
        cls,
        player_obj: PlayerModel,
        item_obj: ItemModel,
        inv_obj: InventoryModel,
        quantity: int,
    ) -> Tuple[int, int]:

        sold_price = item_obj.cost * quantity
        new_q = inv_obj.quantity - quantity
        curr_bal = player_obj.balance
        new_bal = sold_price + curr_bal

        if new_q == 0:
            await inv_obj.delete()
        else:
            await inv_obj.update(quantity=new_q).apply()

        await player_obj.update(balance=new_bal).apply()

        return sold_price, new_bal

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
