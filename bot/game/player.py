import math
import random
from typing import Tuple, Union, List

import ujson

from bot.database.models import Player as PlayerModel
from dataclasses import dataclass

with open("levels.json", "r") as f:
    LEVELS = ujson.load(f)


def level_energy_usage(level: int):
    return 1 / 10 * pow((1 + 1 / 50), level + 40) + 10


def energy_increase(player_level: int):
    if player_level == 1:
        # Prevent issues with nullification and log(1)
        player_level = 2

    return abs(
        level_energy_usage(player_level) * ((player_level / 2) * math.log(player_level))
    )


def plant_tier_formula(tier: int, modifier: float):
    return 10 * pow(1.1, tier + 10 - modifier) - abs(2 * math.log(tier * 2) + 15)


def plant_stage_formula(stage: int, modifier: float):
    return 5 * pow(1.1, stage + 10 - modifier) + 8


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
        player_energy = int(player_db.energy)
        for level, xp in LEVELS.items():
            if player_db.xp >= xp:
                player_level = int(level)
                player_energy = int(player_energy + energy_increase(player_level))
            else:
                break

        await player_db.update(level=player_level, energy=player_energy).apply()

        return (
            player,
            player_level != og_level,
        )

    @classmethod
    async def water_usage(
        cls, player_level: int, plant_tier: int, plant_stage: int, modifier: float = 0
    ) -> int:
        """**Use to calculate water needed for the watering command.**

        USAGE:
        water_needed = await Player.water_usage(
            player_level=10, plant_tier=1, plant_stage=1
        )

        """
        if player_level == 1:
            # Prevent issues with doubling water needed at level 1
            player_level = 2
        return int(
            (
                (
                    plant_tier_formula(plant_stage, modifier)
                    + plant_stage_formula(plant_tier, modifier)
                )
                / ((player_level / 2) * math.log(player_level) + 10)
            )
            * 15
        )

    @classmethod
    async def energy_usage(
        cls, player_level: int, plant_tier: int, plant_stage: int, modifier: float = 1
    ) -> int:
        """**Use to calculate energy needed for any farming command.**

        USAGE:
        energy_needed = await Player.energy_usage(
            player_level=10, plant_tier=1, plant_stage=1
        )

        IMPORTANT: Energy expects a default of 1 for modifier, while water expects a 0. Please do not use modifier
        unless you need it, otherwise allow for default.

        """
        if player_level == 1:
            # Prevent issues with nullification and log(1)
            player_level = 2

        return int(
            abs(
                (
                    modifier
                    * (
                        level_energy_usage(player_level)
                        + plant_stage_formula(plant_stage, modifier)
                        + plant_tier_formula(plant_tier, modifier)
                    )
                )
                * ((player_level / 2) * math.log(player_level))
            )
        )
