import random
from typing import Tuple, Union, List, Optional

import ujson

from bot.database.models import Player as PlayerModel
from bot.database.models import Item as ItemModel
from bot.database.models import Inventory as InventoryModel
from bot.game.inventory import Inventory
from dataclasses import dataclass

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

    @classmethod
    async def sell(cls, item_id: int, player_id: int, quantity: int):
        selling = (
            await InventoryModel.query.where(InventoryModel.id == player_id)
            .update(quantity)
            .where(item_id=item_id)
        )

        return selling

    @classmethod
    async def item(cls, item_id: int):
        item_query = await ItemModel.query.where(ItemModel.item_id == item_id).gino()

        return item_query

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
