import random
from typing import Tuple

import ujson

from bot.database.models import Player as PlayerModel
from dataclasses import dataclass

with open("levels.json", "r") as f:
    LEVELS = ujson.load(f)


@dataclass
class Player:
    id: int
    balance: int
    xp: int
    level: int
    energy: int

    @classmethod
    async def load(cls, user_id: int, guild_id: int):
        player = (
            await PlayerModel.query.where(PlayerModel.user_id == user_id)
                .where(PlayerModel.guild_id == guild_id)
                .gino.first()
        )
        if player is None:
            player = await PlayerModel.create(user_id=user_id, guild_id=guild_id)
        return Player(
            id=player.id,
            balance=player.balance,
            xp=player.xp,
            level=player.level,
            energy=player.energy,
        )

    @classmethod
    async def update_xp(cls, user_id, guild_id, modifier) -> Tuple["Player", bool]:
        """**Use to give XP after a successful command.**

        USAGE:
        player, levelled_up = await Player.update_xp(
            user_id=message.author.id, guild_id=message.guild.id, modifier=0
        )

        """
        player = (
            await PlayerModel.query.where(PlayerModel.user_id == user_id)
                .where(PlayerModel.guild_id == guild_id)
                .gino.first()
        )
        if player is None:
            player = await PlayerModel.create(user_id=user_id, guild_id=guild_id)

        modifier += 0.1

        if player.level > 4:
            xp = player.xp + abs(
                int(
                    (
                            (
                                    (
                                            1
                                            * random.randint(1, 10)
                                            * abs(player.level - (player.level * 0.4))
                                    )
                                    / (5 * 1)
                            )
                            * (
                                    (
                                            pow(((2 * abs(player.level - (player.level * 0.4))) + 10), 2.5)
                                            / pow(
                                        (
                                                abs(player.level - (player.level * 0.4))
                                                + player.level
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
            xp = player.xp + abs(random.randint(1, 5))

        await player.update(xp=xp).apply()

        og_level = player.level

        player_level = 1
        for level in LEVELS.keys():
            if player.xp >= LEVELS[level]:
                player_level = level

        await player.update(level=int(player_level)).apply()

        return await Player.load(user_id=user_id, guild_id=guild_id), player_level != og_level