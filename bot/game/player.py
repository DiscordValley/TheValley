from typing import List

from bot.database.models import Player as PlayerModel
from dataclasses import dataclass


@dataclass
class Player:
    id: int
    balance: int
    xp: int
    level: int
    energy: int

    @classmethod
    async def load(
        cls, user_id: int = None, guild_id: int = None, player_obj: PlayerModel = None
    ):
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
    async def top(cls, guild_id: int) -> List["Player"]:
        leaders = (
            await PlayerModel.query.where(PlayerModel.guild_id == guild_id)
            .order_by(PlayerModel.xp.desc())
            .limit(5)
            .gino.all()
        )
        print(leaders)
        players = list()
        for leader in leaders:
            players.append(await Player.load(player_obj=leader))
        return players
